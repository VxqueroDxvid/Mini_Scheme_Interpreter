from schemeVisitor import schemeVisitor
from schemeParser import schemeParser


class SchemeInterpreter(schemeVisitor):
    def __init__(self):
        # Entorno global que almacena variables y funciones
        self.global_env = {}

    def visitRoot(self, ctx):
        # Procesa el nodo raíz del programa
        results = []
        for child in ctx.children:
            if isinstance(child, schemeParser.DeclarationContext):
                self.visit(child)  # Procesa declaraciones (define)
            elif isinstance(child, schemeParser.ExprContext):
                if child.func_declaration():
                    self.visit(child)  # Procesa definiciones de funciones
                else:
                    result = self.visit(child)  # Procesa expresiones
                    if result is not None:
                        results.append(result)
        return results

    def visitDeclaration(self, ctx):
        # Trata declaraciones "define" y las guarda en el entorno global
        var_name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.global_env[var_name] = value
        return value

    def visitExpr(self, ctx):
        # Procesa literales
        if ctx.literal():
            return self.visitLiteral(ctx.literal())

        # Procesa identificadores (variables)
        if ctx.ID():
            var_name = ctx.ID().getText()
            if var_name in self.global_env:
                value = self.global_env[var_name]
                if isinstance(value, tuple):  # Si es una función
                    return value
                return int(value) if isinstance(
                    value, str) and value.isdigit() else value
            raise ValueError(f"Variable no definida: {var_name}")

        # Procesa definiciones de funciones
        if ctx.func_declaration():
            func_name = ctx.func_declaration().ID(0).getText()
            params = [p.getText() for p in ctx.func_declaration().ID()[1:]]
            body_ctx = ctx.func_declaration().expr()
            self.global_env[func_name] = (params, body_ctx)
            return None

        # Procesa llamadas a funciones
        if ctx.func_invocation():
            func_name = ctx.func_invocation().ID().getText()
            arguments = [self.visit(arg)
                         for arg in ctx.func_invocation().expr()]
            if func_name in self.global_env:
                func = self.global_env[func_name]
                if isinstance(func, tuple):  # Función definida por el usuario
                    return self._evaluate_user_function(func_name, arguments)
                elif callable(func):  # Función predefinida
                    return func(*arguments)
                raise ValueError(f"'{func_name}' no es una función válida.")
            raise ValueError(f"Función no definida: {func_name}")

        # Procesa display para mostrar valores
        if ctx.DISPLAY():
            value_to_display = self.visit(ctx.expr(0))
            if isinstance(value_to_display, list):  # Formatea listas
                value_to_display = f"({ ' '.join(map(str, value_to_display)) })"
            print(value_to_display)
            return None

        # Procesa saltos de línea
        if ctx.NEWLINE():
            print("")
            return None

        # Procesa lectura de valores
        if ctx.READ():
            user_input = input("Introduce un valor: ")
            try:
                return int(user_input)
            except ValueError:
                return user_input

        # Procesa operadores para listas
        if ctx.CAR() or ctx.CDR() or ctx.CONS() or ctx.NULLP():
            operator = (
                "car" if ctx.CAR() else
                "cdr" if ctx.CDR() else
                "cons" if ctx.CONS() else
                "null?"
            )
            arguments = [self.visit(expr) for expr in ctx.expr()]
            return self._evaluate_list_operator(operator, arguments)

        # Procesa operadores lógicos y aritméticos
        if ctx.logical_operator() or ctx.operator():
            operator = ctx.logical_operator() or ctx.operator()
            arguments = [self.visit(arg) for arg in ctx.expr()]
            if ctx.logical_operator():
                return self._evaluate_logical(operator.getText(), arguments)
            else:
                return self._evaluate_arithmetic(operator.getText(), arguments)

        # Procesa condicionales if y cond
        if ctx.if_clause():
            return self._evaluate_if(ctx.if_clause())
        if ctx.cond_clause():
            return self._evaluate_cond(ctx.cond_clause())

        # Procesa declaraciones let
        if ctx.let_binding():
            return self._evaluate_let(ctx)

        raise ValueError(f"Operador o función no reconocido: {ctx.getText()}")

    def _evaluate_logical(self, operator, arguments):
        # Evalúa operadores lógicos and, or, not
        if operator == 'and':
            return "#t" if all(arg == "#t" for arg in arguments) else "#f"
        if operator == 'or':
            return "#t" if any(arg == "#t" for arg in arguments) else "#f"
        if operator == 'not':
            return "#t" if arguments[0] == "#f" else "#f"

    def _evaluate_arithmetic(self, operator, arguments):
        # Evalúa operadores aritméticos y relacionales
        if operator == '+':
            return sum(arguments)
        if operator == '-':
            return arguments[0] - sum(arguments[1:])
        if operator == '*':
            result = 1
            for arg in arguments:
                result *= arg
            return result
        if operator == '/':
            result = arguments[0]
            for arg in arguments[1:]:
                result /= arg
            return result
        if operator == 'mod':
            if len(arguments) != 2:
                raise ValueError(
                    "El operador 'mod' requiere exactamente 2 argumentos.")
            return arguments[0] % arguments[1]
        if operator in ('<', '>', '<=', '>=', '=', '<>'):
            return self._evaluate_relational(operator, arguments)

    def _evaluate_relational(self, operator, arguments):
        # Evalúa operadores relacionales
        left, right = arguments
        if operator == '<':
            return "#t" if left < right else "#f"
        if operator == '>':
            return "#t" if left > right else "#f"
        if operator == '<=':
            return "#t" if left <= right else "#f"
        if operator == '>=':
            return "#t" if left >= right else "#f"
        if operator == '=':
            return "#t" if left == right else "#f"
        if operator == '<>':
            return "#t" if left != right else "#f"

    def _evaluate_if(self, ctx):
        # Evalúa el condicional if
        condition_ctx = ctx.expr(0)
        true_ctx = ctx.expr(1)
        false_ctx = ctx.expr(2)
        condition_value = self.visit(condition_ctx)
        if condition_value == "#t" or condition_value is True:
            return self.visit(true_ctx)
        elif condition_value == "#f" or condition_value is False:
            return self.visit(false_ctx)
        else:
            raise ValueError(f"Condición no válida en 'if': {condition_value}")

    def _evaluate_cond(self, ctx):
        # Evalúa el condicional cond
        for clause in ctx:
            if clause.ELSE():
                result = None
                for expr_ctx in clause.expr():
                    result = self.visit(expr_ctx)
                return result
            condition = self.visit(clause.expr(0))
            if condition == "#t":
                result = None
                for expr_ctx in clause.expr()[1:]:
                    result = self.visit(expr_ctx)
                return result

    def _evaluate_let(self, ctx):
        # Evalúa declaraciones let
        local_env = self.global_env.copy()
        for binding in ctx.let_binding():
            var_name = binding.ID().getText()
            var_value = self.visit(binding.expr())
            local_env[var_name] = var_value
        previous_env = self.global_env
        self.global_env = local_env
        try:
            result = None
            for expr in ctx.expr():
                result = self.visit(expr)
        finally:
            self.global_env = previous_env
        return result

    def _evaluate_list_operator(self, operator, arguments):
        # Para los operadores de las listas
        if operator == "car":
            if not arguments or not isinstance(arguments[0], list):
                raise ValueError("car requiere una lista no vacía.")
            return arguments[0][0]
        elif operator == 'cdr':
            if not arguments[0]:
                return []
            if isinstance(arguments[0], list):
                return arguments[0][1:]
            else:
                raise ValueError("cdr solo se puede aplicar a listas")
        elif operator == "cons":
            if len(arguments) != 2 or not isinstance(arguments[1], list):
                raise ValueError("cons requiere un elemento y una lista.")
            return [arguments[0]] + arguments[1]
        elif operator == 'null?':
            if arguments[0] == [] or arguments[0] == '()':
                return "#t"
            return "#f"

    def _evaluate_user_function(self, func_name, arguments):
        # Para las funciones definidas por el usuario
        params, body_ctx_list = self.global_env[func_name]
        if len(params) != len(arguments):
            raise ValueError("Número de argumentos no coincide")
        local_env = self.global_env.copy()
        for param, arg in zip(params, arguments):
            local_env[param] = arg
        previous_env = self.global_env
        self.global_env = local_env
        try:
            result = None
            for expr_ctx in body_ctx_list:
                result = self.visit(expr_ctx)
        finally:
            self.global_env = previous_env
        return result

    def visitLiteral(self, ctx):
        # Convierte literales a sus valores correspondientes
        if ctx.NUMBER():
            return int(ctx.NUMBER().getText())
        elif ctx.BOOLEAN():
            return "#t" if ctx.BOOLEAN().getText() == '#t' else "#f"
        elif ctx.STRING():
            return ctx.STRING().getText()
        elif ctx.quoted_list():
            return self.visitQuoted_list(ctx.quoted_list())

    def visitQuoted_list(self, ctx):
        # Procesa listas literales precedidas por un apóstrofe
        try:
            if ctx.LPAR() and ctx.RPAR():  # Verifica que hay paréntesis válidos
                return [self.visitLiteral(literal)
                        for literal in ctx.literal()]
            else:
                raise ValueError(
                    "Error: El apóstrofe debe ir seguido de una lista válida entre paréntesis.")
        except Exception as e:
            raise ValueError(f"Error procesando lista con apóstrofe: {str(e)}")
