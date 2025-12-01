



class Processo:
    def __init__(self, pid):
        self.pid = pid
        self.relogio = 0  # Passo 1: Relógio lógico iniciado em 0

    def __repr__(self):
        return f"{self.pid} (Relógio: {self.relogio})"

    def log(self, tipo_evento, detalhes=""):
        """Função auxiliar apenas para imprimir o estado atual."""
        print(f"[{self.pid}] Relógio Atualizado: {self.relogio:02d} | Evento: {tipo_evento} {detalhes}")

    def evento_interno(self):
        # Passo 2 : Antes de executar, incrementa L_i
        self.relogio += 1
        self.log("Evento Interno")

    def enviar_mensagem(self, destinatario_pid):
        # Passo 2 : Incrementa antes de enviar
        self.relogio += 1
        
        # Passo 3 : a mensagem  inclui timestamp t = L_i
        timestamp_msg = self.relogio
        
        self.log("Envio de Msg", f"-> Para {destinatario_pid} (Levando Ts: {timestamp_msg})")
        
        # Retorna mensagem com o timestamp para ser usada no recebimento
        return {"conteudo": "Olá", "timestamp": timestamp_msg, "remetente": self.pid}

    def receber_mensagem(self, pacote_mensagem):
        timestamp_recebido = pacote_mensagem["timestamp"]
        remetente = pacote_mensagem["remetente"]
        
        # Passo 4 : Primeiro ajusta L_j = max(L_j, t)
        self.relogio = max(self.relogio, timestamp_recebido)
        
        # Depois aplica Regra 1: incrementa L_j antes de processar
        self.relogio += 1
        
        self.log("Recebimento", f"<- De {remetente} (Ts da msg: {timestamp_recebido})")


# --- Passo 5: Simulação da Sequência de Eventos ---

def executar_simulacao():
    print("--- Início da Simulação de Lamport ---\n")
    
    # Criando os processos
    p1 = Processo("P1")
    p2 = Processo("P2")
    p3 = Processo("P3")

    # Executando a sequência exata da imagem:
    
    # 1. P1: Evento interno.
    p1.evento_interno()
    
    # 2. P2: Envia mensagem para P3.
    msg_p2_para_p3 = p2.enviar_mensagem("P3")
    
    # 3. P3: Recebe mensagem de P2.
    p3.receber_mensagem(msg_p2_para_p3)
    
    # 4. P1: Envia mensagem para P2.
    msg_p1_para_p2 = p1.enviar_mensagem("P2")
    
    # 5. P3: Evento interno.
    p3.evento_interno()
    
    # 6. P2: Recebe mensagem de P1.
    p2.receber_mensagem(msg_p1_para_p2)
    
    # 7. P2: Envia mensagem para P1.
    msg_p2_para_p1 = p2.enviar_mensagem("P1")
    
    # 8. P1: Recebe mensagem de P2.
    p1.receber_mensagem(msg_p2_para_p1)

    print("\n--- Estado Final dos Processos ---")
    print(p1)
    print(p2)
    print(p3)

if __name__ == "__main__":
    executar_simulacao()