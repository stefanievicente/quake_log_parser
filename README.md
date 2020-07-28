# quake_log_parser

Construa um Parser para o arquivo de log. 
O arquivo "Quake.txt" é gerado pelo servidor de Quake 3 Arena. Nele está registrado informações sobre as partidas, informações como: Quando começa, quando termina, quem matou quem, quem "se matou" (caiu no vazio, explodiu a si próprio), entre outros. O Parser deve ser capaz de ler o arquivo, agrupar os dados de cada partida, e organizar as suas informações.
 
Exemplo:
21:42 Kill: 1022 2 22: <world> killed Isgalamido by MOD_TRIGGER_HURT
* O player "Isgalamido" morreu por que estava ferido e caiu de uma altura que o matou.
 2:22 Kill: 3 2 10: Isgalamido killed Dono da Bola by MOD_RAILGUN
* O player "Isgalamido" matou o player "Dono da Bola" usando a arma "Railgun".
Para cada jogo o Parser deve gerar algo como: 
[{
  "game": 1,
  "status": {
     "total_kills": 45,
     "players": [
		{
			"id": 1,
			"nome": "Mocinha",
			"kills": 5,
			"old_names": ["Dono da bola"]
		},
		{
			"id": 2,
			"nome": "Isgalamido",
			"kills": 18,
			"old_names": []
		},
		{
			"id": 3,
			"nome": "Zeh",
			"kills": 20,
			"old_names": []
		}
	]
  }
}]
Observações: Quando o <world> mata o player ele perde -1 kill. <world> não é um player e não deve aparecer na lista de players e nem no dicionário de kills. total_kills são os kills dos games, isso inclui mortes do <world>.
O Comando ClientUserinfoChanged indica a definição do nome do jogador.
