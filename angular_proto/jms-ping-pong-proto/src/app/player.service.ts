import { Injectable } from '@angular/core';
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

  private playersUrl = 'api/players';  // URL to web api
  private statisticUrl = 'api/statistic';  // URL to web api

  /** GET players from the server */
  getPlayers(): Observable<Player[]> {
    return this.http.get<Player[]>(this.playersUrl)
  }

  getStatistics(first_id: number, second_id: number): Observable<Statistic> {
    // In memory web API doesn't handle this case:
    // var requestUrl = this.statisticUrl + '/' + first_id + '/' + second_id;
    //   return this.http.get<Statistic>(requestUrl)

    // So just returning results as if we had web communication.
    var statistic: Statistic = {winner_id: 0, winner_probability: 0.0};

    // Yes, I'm being lazy and not including math for abs.
    var abs_difference = 0;
    if (first_id > second_id)
    {
      statistic.winner_id = first_id;
      abs_difference = first_id - second_id;
    }
    else
    {
      statistic.winner_id = second_id;
      abs_difference = second_id - first_id;
    }

    if (abs_difference > 10)
    {
      statistic.winner_probability = 0.8;
    }
    else
    {
      statistic.winner_probability = 0.6;
    }

    var returnValue = of(statistic);
    return returnValue;
  }

}
