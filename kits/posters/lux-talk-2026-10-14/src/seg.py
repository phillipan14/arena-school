import sys, Vision, Quartz
from Foundation import NSURL
import numpy as np
from PIL import Image
def segment(inp, out):
    url=NSURL.fileURLWithPath_(inp)
    src=Quartz.CGImageSourceCreateWithURL(url,None); cg=Quartz.CGImageSourceCreateImageAtIndex(src,0,None)
    req=Vision.VNGeneratePersonSegmentationRequest.alloc().initWithCompletionHandler_(None)
    req.setQualityLevel_(Vision.VNGeneratePersonSegmentationRequestQualityLevelAccurate)
    h=Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(cg,None)
    ok,err=h.performRequests_error_([req],None); assert ok,err
    pb=req.results()[0].pixelBuffer()
    Quartz.CVPixelBufferLockBaseAddress(pb,0)
    w=Quartz.CVPixelBufferGetWidth(pb); hh=Quartz.CVPixelBufferGetHeight(pb); bpr=Quartz.CVPixelBufferGetBytesPerRow(pb)
    buf=Quartz.CVPixelBufferGetBaseAddress(pb).as_buffer(bpr*hh)
    m=np.frombuffer(buf,dtype=np.uint8).reshape(hh,bpr)[:, :w].copy()
    Quartz.CVPixelBufferUnlockBaseAddress(pb,0)
    im=Image.open(inp).convert('RGB')
    mask=Image.fromarray(m).resize(im.size, Image.LANCZOS)
    rgba=im.copy(); rgba.putalpha(mask); rgba.save(out); print(out, im.size, 'mask', (w,hh))
segment(sys.argv[1], sys.argv[2])
