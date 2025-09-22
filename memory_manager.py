class MemoryManager:
    def __init__(self):
        pass

    def simulate_memory_management(self, algorithm, page_list, frame_size):
        from page_replacement import FIFO, LRU, Optimal

        if algorithm == "FIFO":
            raw = FIFO(page_list, frame_size)
        elif algorithm == "LRU":
            raw = LRU(page_list, frame_size)
        elif algorithm == "Optimal":
            raw = Optimal(page_list, frame_size)
        else:
            raise ValueError("Unknown algorithm selected")

        return [{
            "step": step,
            "page": page,
            "frames": frames,
            "page_fault": "Yes" if page_fault else "No"
        } for step, page, frames, page_fault in raw]

    def compare_all_algorithms(self, page_list, frame_size):
        from page_replacement import FIFO, LRU, Optimal
        algorithms = {
            "FIFO": FIFO(page_list, frame_size),
            "LRU": LRU(page_list, frame_size),
            "Optimal": Optimal(page_list, frame_size),
        }

        formatted_results = {}
        for name, results in algorithms.items():
            formatted_results[name] = [{
                "step": step,
                "page": page,
                "frames": frames,
                "page_fault": "Yes" if page_fault else "No"
            } for step, page, frames, page_fault in results]

        return formatted_results

