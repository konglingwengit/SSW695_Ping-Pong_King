import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment'

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebService {

  constructor(
    private http: HttpClient) { }

  private playersUrl = environment.webapiurl + '/players';  // URL to web api
  private predictionUrl = environment.webapiurl + '/predictions';  // URL to web api
  private singlePlayerStatsUrl = environment.webapiurl + '/single_player_stats';  // URL to web api
  private matchStatsUrl = environment.webapiurl + '/vs_stats';  // URL to web api


  /** GET players from the server */
  getPlayers(): Observable<any []> {
    return this.http.get<any []>(this.playersUrl)
  }

  getPredictions(first_id: number, second_id: number, prediction: string): Observable<any> {
    var requestUrl = this.predictionUrl + '?prediction=' + prediction + '&p1=' + first_id + '&p2=' + second_id;
    return this.http.get<any>(requestUrl)
  }

  getIndividualStatistics(first_id: number): Observable<any> {
    var requestUrl = this.singlePlayerStatsUrl + '?p1=' + first_id
    return this.http.get<any>(requestUrl)
  }

  getMatchStatistics(first_id: number, second_id: number): Observable<any> {
    var requestUrl = this.matchStatsUrl + '?p1=' + first_id + '&p2=' + second_id;
    return this.http.get<any>(requestUrl)
  }

}
