# Esse codigo cria uma instancia de SALA apartir das 
# informações que estão no banco de dados.


import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password= '5991',
    database= 'mydatabase'
)



# CLASSE AGENDA
class Agenda:
    def __init__(self):
        self.horarios = {
            '08h00_10h00' : 'Livre',
            '10h00_12h00' : 'Livre',
            '13h30_15h30' : 'Livre',
            '15h30_17h30' : 'Livre',
        }

    def exibir_horarios(self):
        for horario, status in self.horarios.items():
            print(f'{horario}: {status}')

# CLASSE SALA
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


# ACESSA O BANCO DE DADOS PARA OBTER AS INFORMAÇÕES
def create_sala_from_db(ID_Sala):
    cursor = conexao.cursor()

    # Obter informações da sala
    command = f'SELECT Nome, Capacidade, ID_Agenda FROM Sala WHERE ID_Sala = {ID_Sala}'
    cursor.execute(command)
    Nome, Capacidade, ID_Agenda = cursor.fetchone()

    # Obter informações da agenda
    command = f'SELECT Segunda, Terca, Quarta, Quinta, Sexta FROM Agenda WHERE ID_Agenda = {ID_Agenda}'
    cursor.execute(command)
    ID_Horario_Segunda, ID_Horario_Terca, ID_Horario_Quarta, ID_Horario_Quinta, ID_Horario_Sexta = cursor.fetchone()

    # Criar objeto de sala
    sala = Sala(Nome, Capacidade)

    # Para cada dia da semana, obter o horário correspondente e preencher a agenda da sala
    for dia, ID_Horario in zip(['segunda', 'terca', 'quarta', 'quinta', 'sexta'], [ID_Horario_Segunda, ID_Horario_Terca, ID_Horario_Quarta, ID_Horario_Quinta, ID_Horario_Sexta]):
        command = f'SELECT 08h00_10h00, 10h00_12h00, 13h30_15h30, 15h30_17h30 FROM Horarios WHERE ID_Horario = {ID_Horario}'
        cursor.execute(command)
        horario = cursor.fetchone()
        
        sala.dias[dia].horarios = {
            '08h00_10h00' : horario[0],
            '10h00_12h00' : horario[1],
            '13h30_15h30' : horario[2],
            '15h30_17h30' : horario[3],
        }

    cursor.close()
    return sala


# TESTE
sala = create_sala_from_db(2)
sala.exibir_sala()
