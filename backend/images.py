"""Decode bounded raster uploads and emit fresh pixels with no source metadata."""
import io
import warnings
from PIL import Image, ImageOps, UnidentifiedImageError
from .service import Problem

MAX_UPLOAD = 5 * 1024 * 1024
MAX_PIXELS = 12_000_000
MAX_STORED = 1024 * 1024

def normalise_image(raw):
    if not isinstance(raw, bytes) or not raw:raise Problem(400,'Choose an image')
    if len(raw)>MAX_UPLOAD:raise Problem(413,'Choose an image up to 5 MB')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(raw), formats=['JPEG','PNG','WEBP']) as source:
                if source.width*source.height>MAX_PIXELS:raise Problem(413,'Image exceeds 12 million pixels')
                if getattr(source,'n_frames',1)!=1:raise Problem(400,'Choose a still image, not an animation')
                source.load()
                oriented=ImageOps.exif_transpose(source)
                oriented.thumbnail((1600,1600),Image.Resampling.LANCZOS)
                # Copy pixels into a new image; never preserve EXIF/GPS/ICC/XMP/text/filename.
                rgba=oriented.convert('RGBA')
                clean=Image.new('RGB',rgba.size,'white');clean.paste(rgba,mask=rgba.getchannel('A'))
                for quality in (85,70,55):
                    out=io.BytesIO();clean.save(out,format='JPEG',quality=quality,optimize=True)
                    if out.tell()<=MAX_STORED:return out.getvalue(),clean.width,clean.height
                raise Problem(413,'Image is too detailed; choose a smaller image')
    except Problem:raise
    except (UnidentifiedImageError,OSError,ValueError,SyntaxError,Image.DecompressionBombWarning,Image.DecompressionBombError):
        raise Problem(400,'Choose a valid still JPG, PNG or WebP image')
