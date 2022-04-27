import socket
#import base64

h = open('index.html', 'r') # abrindo e lendo o html
homepage = h.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(s)

s.bind(('', 12000))
s.listen(5) # quer manter uma fila de 5 conecções, dessa forma ate 5 pessoas podem ficar esperando 

while True:
    conn, addr = s.accept() # aceita a conecção quando alguem entrar no site
    # conn = socket de coneccão. tipo um "ponteiro" que aponta pra quem ta querendo conectar
    # addr = endereço de quem ta tentando se conectar

    data = conn.recv(2000) # o recv recebe os dados de quem está requisitando
    
    P = data.split(b' ') #GET / HTTP/1.0 -> [GET, /, HTTP/1.0]
    #print(P)
    if P[0] == b'GET':
        #print(P[0])
        if P[1] == b'/': #se não tiver nada depois do /, significa que o usuário está procurando a página inicial. Nesse caso, retornamos a pag 
            #print(P[1])
            resp = ('HTTP/1.0 200 OK\r\n' + 'Content-Type: text/html\r\n' + 'Content-Length: ' + str(len(homepage)) + '\r\n\r\n' + (homepage))
            # como resposta ele manda: protocolo http + código da respo (200) + ok (mensagem do codigo) + tipo do conteudo (content-type), falando se é imagem html etc
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
