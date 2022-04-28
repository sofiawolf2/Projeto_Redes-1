import socket

h = open('index.html', 'r') # abrindo e lendo o html, h será a variável que receberá o site 
homepage = h.read() #homepage lê o site e recebe a versão string dele

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# abrindo o socket , onde na função passamos 2 argumentos, AF_INET que declara a família do protocolo , SOCKET_STREAM, indica que será TCP/IP

s.bind(('', 12000)) # Esta linha define para qual IP e porta o servidor deve aguardar a conexão, que no nosso caso é qualquer IP, por isso o Host é ”

s.listen(1)  # Define o limite de conexões.

while True: # roda enquanto tiver conexão
    conn, addr = s.accept() # deixa o Servidor na escuta aguardando as conexões, aceita a conexão quando alguem entrar no site
    # conn = socket de conexão. tipo um "ponteiro" que aponta pra quem ta querendo conectar
    # addr = endereço de quem ta tentando se conectar

    data = conn.recv(2000) # o recv recebe os dados de quem está requisitando
    # 2000 é o número máx de bytes aceitos

    P = data.split(b' ') #GET / HTTP/1.0 -> [GET, /, HTTP/1.0]
    # p vai armazenar os dados recebidos na variavel data, separados por espaços

    if P[0] == b'GET':

        if P[1] == b'/': #se não tiver nada depois do /, significa que o usuário está procurando a página inicial. Nesse caso, retornamos a pag 

            resp = ('HTTP/1.0 200 OK\r\n' + 'Content-Type: text/html\r\n' + 'Content-Length: ' + str(len(homepage)) + '\r\n\r\n' + (homepage))
            # como resposta ele manda: protocolo http + código da resposta (200) + ok (mensagem do codigo) + tipo do conteudo (content-type), falando se é imagem html etc
            # + tamanho do conteudo (content-length), a quantidade de bytes q ele tem + depois de 2 pular linha, o conteúdo em si, ou seja a página. 
            # Se fosse uma imagem, seria uma imagem. nesse caso é a página.
            resp = str.encode(resp) #encode() é uma função que transforma a string em byte
            conn.sendall(resp) #manda de volta pra pessoa

        else: # em qualquer outro caso, retornamos o que o usuário ta procurando
            try: # caso não exista o que o usuário ta procurando, o try except lida com isso 
                print('file was sent: ' + str(P[1]))
                ext = str(P[1].rpartition(b'.')[-1]) # ele está pegando o último do array string para saber qual o tipo do arquivo 
                f = open(P[1][1:], 'rb') # abre o arquivo e ler em bytes, pois ele pode receber qualquer tipo de aquivo, n só string
                figure = f.read()
                conn.sendall(b'HTTP/1.0 200 OK\r\n Content-Type: file' + ext.encode() + b'\r\n' +
                             b'Content-Length: ' + str(len(figure)).encode() + b'\r\n\r\n' +
                              figure)
            except:
                # se não achar, será emitido um erro 404 NOT FOUND
                msg = b'Arquivo N Encontrado :/'
                conn.sendall(b'HTTP/1.0 404 NOT FOUND\r\n Content-Type: file' + ext.encode() + b'\r\n' +
                         b'Content-Length: ' + str(len(msg)).encode() + b'\r\n\r\n' + msg)

                # O código n estava conseguindo rodar pois n tava conseguindo concatenar string + bytes. Nesse caso, transformamos tudo em byte
    
    conn.close()
s.close()
