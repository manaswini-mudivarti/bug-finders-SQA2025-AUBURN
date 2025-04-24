import functools, logging, time
logging.basicConfig(filename="forensics.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

def forensic_tracking(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = fn(*args, **kwargs)
            status = "OK"
            return result
        except Exception as e:
            status = f"EXCEPTION: {type(e).__name__}"
            raise
        finally:
            duration = int((time.time() - start) * 1000)
            logging.info(f"{fn.__module__}.{fn.__name__} | status={status} | "
                         f"args={args} kwargs={kwargs} | "
                         f"duration_ms={duration}")
    return wrapper
