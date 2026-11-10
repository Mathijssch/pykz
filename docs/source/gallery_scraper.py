"""Isolate PyKZ state and PDF outputs between Sphinx-Gallery examples."""

from pathlib import Path
import shutil


class PDFScraper:
    def __init__(self):
        self._directory = None
        self._snapshots = {}

    def _snapshot(self):
        return {
            path: (stat.st_mtime_ns, stat.st_ctime_ns, stat.st_size)
            for path in self._directory.glob("*.pdf")
            for stat in [path.stat()]
        }

    def reset(self, gallery_conf, filename):
        """Run before each example, including before its first code block."""
        from pykz.api import WorkSpace

        WorkSpace.scf(None)
        WorkSpace.sca(None)
        path = Path(filename)
        if not path.is_absolute():
            # Sphinx-Gallery passes only the example basename to reset hooks.
            directories = gallery_conf["examples_dirs"]
            if isinstance(directories, str):
                directories = [directories]
            candidates = [
                candidate
                for directory in directories
                for candidate in (Path(gallery_conf["src_dir"]) / directory).rglob(path.name)
            ]
            if len(candidates) != 1:
                raise RuntimeError(f"Cannot uniquely locate gallery example {filename}")
            path = candidates[0]
        self._directory = path.resolve().parent
        self._snapshots = self._snapshot()

    def __call__(self, block, block_vars, gallery_conf):
        import pdf2image
        from sphinx_gallery.scrapers import figure_rst

        directory = Path(block_vars["src_file"]).resolve().parent
        if directory != self._directory:
            raise RuntimeError("PDFScraper.reset must run before each example")
        current = self._snapshot()
        images = []
        for pdf, signature in sorted(current.items()):
            if self._snapshots.get(pdf) == signature:
                continue
            image = Path(next(block_vars["image_path_iterator"]))
            pdf2image.convert_from_path(
                str(pdf), single_file=True, paths_only=True, transparent=False,
                output_file=image.stem, output_folder=str(image.parent),
                dpi=500, fmt="png",
            )
            if not image.is_file():
                raise RuntimeError(f"PDF conversion did not produce {image}")
            shutil.copyfile(pdf, image.with_suffix(".pdf"))
            images.append(str(image))
        self._snapshots = current
        return figure_rst(images, gallery_conf["src_dir"])
