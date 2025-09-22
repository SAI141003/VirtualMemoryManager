from collections import deque

def FIFO(pages, frame_size):
    frames = []
    queue = deque()
    results = []

    for step, page in enumerate(pages):
        page_fault = False
        if page not in frames:
            page_fault = True
            if len(frames) < frame_size:
                frames.append(page)
                queue.append(page)
            else:
                removed_page = queue.popleft()
                frames.remove(removed_page)
                frames.append(page)
                queue.append(page)
        results.append((step + 1, page, list(frames), page_fault))

    return results

def LRU(pages, frame_size):
    frames = []
    usage_order = []
    results = []

    for step, page in enumerate(pages):
        page_fault = False
        if page in frames:
            usage_order.remove(page)
        else:
            page_fault = True
            if len(frames) < frame_size:
                frames.append(page)
            else:
                lru_page = usage_order.pop(0)
                frames.remove(lru_page)
                frames.append(page)
        usage_order.append(page)
        results.append((step + 1, page, list(frames), page_fault))

    return results

def Optimal(pages, frame_size):
    frames = []
    results = []

    for step, page in enumerate(pages):
        page_fault = False
        if page not in frames:
            page_fault = True
            if len(frames) < frame_size:
                frames.append(page)
            else:
                future_use = {}
                for f in frames:
                    try:
                        next_index = pages[step + 1:].index(f)
                    except ValueError:
                        next_index = float('inf')
                    future_use[f] = next_index

                to_remove = max(future_use, key=future_use.get)
                frames.remove(to_remove)
                frames.append(page)
        results.append((step + 1, page, list(frames), page_fault))

    return results

