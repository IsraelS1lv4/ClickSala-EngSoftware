from classAgenda import Agenda

class Sala:
    def __init__(self, Nome, Capacidade):
        self.Nome = Nome
        self.Capacidade = Capacidade
        self.dias = {
            'segunda' : Agenda(),
            'terca'   : Agenda(),
            'quarta'  : Agenda(),
            'quinta'  : Agenda(),
            'sexta'   : Agenda()
        }
        
    def is_available(self, Dias_Aula, Horario_Aulas):
        # Verificar se a sala está disponível nos dias e horários que a turma precisa
        for dia in Dias_Aula:
            for horario in Horario_Aulas:
                if self.dias[dia].horarios[horario] not in ['Livre', None]:
                    return False
        return True
    
    def allocate(self, turma):
        # Verificar se a sala está disponível
        if self.is_available(turma.Dias_Aula, turma.Horario_Aulas):
            # Alocar a turma na sala
            for dia in turma.Dias_Aula:
                for horario in turma.Horario_Aulas:
                    self.dias[dia].horarios[horario] = turma.Nome

    def exibir_sala(self):
        print(f'Nome: {self.Nome}')
        print(f'Capacidade: {self.Capacidade}')
        for dia, agenda in self.dias.items():
            print(f'\nAgenda para {dia}:')
            agenda.exibir_horarios()