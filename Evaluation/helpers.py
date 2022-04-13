class Helpers:
    @staticmethod
    def evaluate(code, n):
        if code < 10000000:
            return False
        
        if n < 5000 and n > 15000:
            return False
        
        return True

    @staticmethod
    def splitRequest(request):
        code, n = request.split('&')
        return int(code), int(n)
