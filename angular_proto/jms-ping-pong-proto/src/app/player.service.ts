import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment'
import { Player } from './player';
import { Statistic } from './statistic';

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PlayerService {

  constructor(
    private http: HttpClient) { }

  private playersUrl = environment.webapiurl + '/players';  // URL to web api
  private statisticUrl = environment.webapiurl + '/predictions';  // URL to web api

  /** GET players from the server */
  getPlayers(): Observable<Player[]> {
    return this.http.get<Player[]>(this.playersUrl)
  }

  getStatistics(first_id: number, second_id: number): Observable<Statistic> {
    var requestUrl = this.statisticUrl + '?prediction=WINNER' + '?p1=' + first_id + '?p2=' + second_id;
    return this.http.get<Statistic>(requestUrl)
  }

}
