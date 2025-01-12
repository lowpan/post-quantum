# Passos de reprodutibilidade


**Requisitos**
* Ubuntu LTS +20.04 (22.04 - preferable)
* Containernet - https://github.com/ramonfontes/containernet
* +6.0.0 kernel

## Gerar arquivos PCAP

### Sem Criptografia

1. Executar o arquivo `topo.py` conforme abaixo:

`sudo python topo.py`


### RSA

2. Executar o arquivo `topo.py` conforme abaixo:

`sudo python topo.py rsa`


### Crystals Kyber

3. Executar o arquivo `topo.py` conforme abaixo:

`sudo python topo.py kyber`


### Gerando resultados

4. Executar o arquivo `graph.py` conforme abaixo:

`sudo python graph.py`

A execução do script `graph.py` resultará em um resultado similar ao apresentado abaixo:

```commandline
Chave Pública kyber: 1244
Chave Pública kyber: 1244
Chave Privada kyber: 1148
DIS kyber: 91
DIS kyber: 91
DIO kyber: 121
DAO kyber: 127
DAOACK kyber: 108
DIO kyber: 121
DIO kyber: 121
DAO kyber: 146
DAOACK kyber: 108
DIO kyber: 121
DIO kyber: 121
DAO kyber: 163
DAOACK kyber: 108
DIO kyber: 121
DIO kyber: 121
DAO kyber: 163
DAOACK kyber: 108
DIO kyber: 121
DIO kyber: 121
DAO kyber: 163
DAOACK kyber: 108
DIO kyber: 121
DIO kyber: 121
DAO kyber: 163
DAOACK kyber: 108
DIO kyber: 121
DIO kyber: 121
DAO kyber: 163
DAOACK kyber: 108
DIO kyber: 121
DIO kyber: 121
DAO kyber: 163
DAOACK kyber: 108
DIO kyber: 121
DIO kyber: 121
DAO kyber: 163
DAOACK kyber: 108
DIO kyber: 121
DIO kyber: 121
DAO kyber: 163
DAOACK kyber: 108
DIO kyber: 121
DIO kyber: 121
DAO kyber: 163
DAOACK kyber: 108
DIO kyber: 121
DIO kyber: 121
Chave Pública rsa: 76
Chave Pública rsa: 76
Chave Privada rsa: 188
DIS rsa: 91
DIS rsa: 91
DIO rsa: 121
DAO rsa: 127
DAOACK rsa: 108
DIO rsa: 121
DIO rsa: 121
DAO rsa: 146
DAOACK rsa: 108
DIO rsa: 121
DIO rsa: 121
DAO rsa: 163
DAOACK rsa: 108
DIO rsa: 121
DIO rsa: 121
DAO rsa: 163
DAOACK rsa: 108
DIO rsa: 121
DIO rsa: 121
DAO rsa: 163
DAOACK rsa: 108
DIO rsa: 121
DIO rsa: 121
DAO rsa: 163
DAOACK rsa: 108
DIO rsa: 121
DIO rsa: 121
DAO rsa: 163
DAOACK rsa: 108
DIO rsa: 121
DIO rsa: 121
DAO rsa: 163
DAOACK rsa: 108
DIO rsa: 121
DIO rsa: 121
DAO rsa: 163
DAOACK rsa: 108
DIO rsa: 121
DIO rsa: 121
DAO rsa: 163
DAOACK rsa: 108
DIO rsa: 121
DIO rsa: 121
DAO rsa: 163
DAOACK rsa: 108
DIS sem_criptografia: 62
DIS sem_criptografia: 62
DIO sem_criptografia: 100
DAO sem_criptografia: 100
DAOACK sem_criptografia: 80
DIO sem_criptografia: 100
DIO sem_criptografia: 100
DAO sem_criptografia: 120
DAOACK sem_criptografia: 80
DIO sem_criptografia: 100
DIO sem_criptografia: 100
DAO sem_criptografia: 140
DAOACK sem_criptografia: 80
DIO sem_criptografia: 100
DIO sem_criptografia: 100
DAO sem_criptografia: 140
DAOACK sem_criptografia: 80
DIO sem_criptografia: 100
DIO sem_criptografia: 100
DAO sem_criptografia: 140
DAOACK sem_criptografia: 80
DIO sem_criptografia: 100
DIO sem_criptografia: 100
DAO sem_criptografia: 140
DAOACK sem_criptografia: 80
DIO sem_criptografia: 100
DIO sem_criptografia: 100
DAO sem_criptografia: 140
DAOACK sem_criptografia: 80
DIO sem_criptografia: 100
DIO sem_criptografia: 100
DAO sem_criptografia: 140
DAOACK sem_criptografia: 80
DIO sem_criptografia: 100
DIO sem_criptografia: 100
DAO sem_criptografia: 140
DAOACK sem_criptografia: 80
DIO sem_criptografia: 100
DIO sem_criptografia: 100
DAO sem_criptografia: 140
DAOACK sem_criptografia: 80
DIO sem_criptografia: 100
DIO sem_criptografia: 100
DAO sem_criptografia: 140
DAOACK sem_criptografia: 80
DIO sem_criptografia: 100
DIO sem_criptografia: 100
DAO sem_criptografia: 140
DAOACK sem_criptografia: 80

```

E na figura a seguir:

![](https://raw.githubusercontent.com/lowpan/post-quantum/refs/heads/main/resultado.png)