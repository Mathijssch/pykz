import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace

import pykz


def test_gallery_isolates_outputs_and_workspace(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "gallery_scraper",
        Path(__file__).parents[1] / "docs/source/gallery_scraper.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    scraper = module.PDFScraper()
    stale = tmp_path / "boxplot.pdf"
    stale.write_bytes(b"previous example")
    pykz.figure()
    pykz.boxplot(1, 2, 3, 4, 5)
    (tmp_path / "contours.py").touch()
    scraper.reset({"examples_dirs": [str(tmp_path)], "src_dir": str(tmp_path)}, "contours.py")
    assert pykz.gcf() is None
    assert pykz.gca() is None

    converted = []

    def convert(pdf, **kwargs):
        converted.append(Path(pdf).name)
        (Path(kwargs["output_folder"]) / (kwargs["output_file"] + ".png")).touch()

    monkeypatch.setitem(sys.modules, "pdf2image", SimpleNamespace(convert_from_path=convert))
    monkeypatch.setitem(sys.modules, "sphinx_gallery.scrapers",
                        SimpleNamespace(figure_rst=lambda images, root: images))
    output = tmp_path / "images"
    output.mkdir()
    block_vars = {
        "src_file": str(tmp_path / "contours.py"),
        "image_path_iterator": iter(str(output / f"image_{i}.png") for i in range(5)),
    }
    conf = {"src_dir": str(tmp_path)}
    assert scraper(None, block_vars, conf) == []
    contour = tmp_path / "contour.pdf"
    contour.write_bytes(b"new contour")
    assert len(scraper(None, block_vars, conf)) == 1
    assert converted == ["contour.pdf"]
    assert scraper(None, block_vars, conf) == []
    # An overwrite in a later block is a new image, even with the same filename.
    contour.write_bytes(b"updated contour")
    assert len(scraper(None, block_vars, conf)) == 1
    assert stale.read_bytes() == b"previous example"
    assert contour.exists()
    # A rebuild must ignore all outputs left by the previous run.
    scraper.reset({}, tmp_path / "contours.py")
    assert scraper(None, block_vars, conf) == []
