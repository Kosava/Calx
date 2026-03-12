class CalculatorEngine:

    def __init__(self):
        self.expression = ""
        self.last_result = ""

    def input(self, value):
        # Ako je prethodni rezultat, počni novi unos osim ako je operator
        if self.last_result and value not in ["+", "-", "*", "/"]:
            self.expression = ""
        self.last_result = ""
        
        self.expression += str(value)
        return self.expression

    def clear(self):
        self.expression = ""
        self.last_result = ""
        return "", "0"

    def evaluate(self):
        try:
            # Evaluiraj izraz
            result = eval(self.expression)
            
            # Formatiraj rezultat
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            result_str = str(result)
            
            # Format: "3+3=6"
            history = f"{self.expression} = {result_str}"
            
            self.last_result = result_str
            self.expression = result_str
            
            return history, result_str
            
        except Exception as e:
            self.expression = ""
            self.last_result = ""
            return "", "Error"