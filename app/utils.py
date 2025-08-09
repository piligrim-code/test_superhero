def parse_filter_param(param: str):
    if not param:
        return None
        
    if ',' in param:
        parts = param.split(',')
        if len(parts) == 2:
            try:
                min_val = int(parts[0]) if parts[0] else None
                max_val = int(parts[1]) if parts[1] else None
                return min_val, max_val
            except ValueError:
                return None
    else:
        try:
            return int(param)
        except ValueError:
            return None
    return None