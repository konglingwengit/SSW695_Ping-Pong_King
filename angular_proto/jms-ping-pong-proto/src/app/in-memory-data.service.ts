import { Injectable } from '@angular/core';
import { InMemoryDbService } from 'angular-in-memory-web-api';
import { Player } from './player';

@Injectable({
  providedIn: 'root',
})
export class InMemoryDataService implements InMemoryDbService {
  createDb() {
    const players = [
      { id: 2, name: 'Jonathan Sebast' },
      { id: 3, name: 'Lingwen Kong' },
      { id: 55, name: 'Deepti Argawal' },
      { id: 66, name: 'Dekun Chen' },
      { id: 77, name: 'Bin Sun' }
    ];
    return {players};
  }
}
