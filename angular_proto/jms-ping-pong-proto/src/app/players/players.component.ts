import { Component, OnInit } from '@angular/core';
import { Player } from '../player';
import { Statistic } from '../statistic';
import { PlayerService } from '../player.service';

@Component({
  selector: 'app-players',
  templateUrl: './players.component.html',
  styleUrls: ['./players.component.css']
})
export class PlayersComponent implements OnInit {

  players: any = [];
  statistic: Statistic = {winner_id: 0, winner_probability: 0};
  firstInput: number = 0;
  secondInput: number = 0;

  constructor(private playerService: PlayerService) {
  }

  getPlayers(): void {
    this.playerService.getPlayers()
      .subscribe(players => this.players = players);
  }

  getStatistics(): void {
    this.playerService.getStatistics(this.firstInput, this.secondInput)
        .subscribe(statistic => this.statistic = statistic);
  }

  getPlayerName(id: number): string {
    for (var player of this.players)
    {
      if (player.id == id)
      {
        return player.name;
      }
    }
    return '';
  }

  ngOnInit(): void {
    this.getPlayers();
  }

}
