import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment'

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
  private addUserUrl = environment.webapiurl + '/user';

  /** GET players from the server */
  getPlayers(): Observable<any []> {
    return this.http.get<any []>(this.playersUrl)
  }

  addUser(email:string): Observable<any []> {
    const postOptions = {
      headers: new HttpHeaders({
        // 'Host': environment.dev_url_prefix + '/',
        // 'Authorization': 'Bearer ' + this.globals.access_token,
        // 'Accept': 'application/json',
        'Content-Type':'application/json',
        'Access-Control-Allow-Origin': '*'
      })
    };
    let data = JSON.stringify({"email":email});
    return this.http.post<any []>(this.addUserUrl,data,postOptions)
  }

  getStatistics(first_id: number, second_id: number, prediction: string): Observable<any> {
    var requestUrl = this.statisticUrl + '?prediction=' + prediction + '&p1=' + first_id + '&p2=' + second_id;
    return this.http.get<any>(requestUrl)
  }

}
