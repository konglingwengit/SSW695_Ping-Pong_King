import { Component, OnInit } from '@angular/core';
import { WebService } from '../web.service';

@Component({
  selector: 'app-players',
  templateUrl: './players.component.html',
  styleUrls: ['./players.component.css']
})
export class PlayersComponent implements OnInit {

  players: any = [{id: 1, name: "Fred"}];
  filtered_players_p1: any = [{id: 1, name: "Fred"}]
  filtered_players_p2: any = [{id: 1, name: "Fred"}]
  statistic: any = [
    // {title: "", line1: "", line2: "", line3: ""}, 
    // {title: "", line1: "", line2: ""}, 
    // {title: "", line1: "", line2: "", line3: ""}, 
    // {title: "", line1: "", line2: ""}, 
    // {title: "", line1: "", line2: "", line3: ""}, 
    // {title: "", line1: "", line2: ""}
  ];
  firstInput: number = 0;
  secondInput: number = 0;
  myFilterP1: string = "";
  myFilterP2: string = "";
  loading: boolean = false;
  barLoading: boolean = false;

  constructor(private webService: WebService) {
  }

  getPlayers(): void {
    this.barLoading = true;
    this.webService.getPlayers()
      .subscribe(players => {
        this.barLoading = false;
        this.updatePlayers(players)
      });
  }

  updatePlayers(input_players: any)
  {
    this.players = input_players;
    this.filterPlayers();
  }

  filterPlayers()
  {
    var filter: string = this.myFilterP1.toLowerCase();
    var filtered_list: any;
    for (let i = 0; i < 2; i++)
    {
      if (filter == "")
      {
        filtered_list = this.players;
      }
      else
      {
        filtered_list = [];
        for (let player of this.players)
        {
          if (player.name.toLowerCase().includes(filter))
          {
            filtered_list.push(player)
          }
        }
      }

      if (i == 0)
        this.filtered_players_p1 = filtered_list;
      else
        this.filtered_players_p2 = filtered_list;

      filter = this.myFilterP2.toLowerCase();
    }

    if (this.filtered_players_p1.length > 0)
    {
      this.firstInput = this.filtered_players_p1[0].id;
    }
    if (this.filtered_players_p2.length > 0)
    {
      this.secondInput = this.filtered_players_p2[0].id;
    }
      

  }

  getPredictions(): void {
    this.loading = true;
    this.webService.getPredictions(this.firstInput, this.secondInput, "ALL")
        .subscribe(statistic => {
          this.loading = false;
          this.statistic = statistic
        });
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
