import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import { PlayersComponent } from './players.component';

describe('PlayersComponent', () => {
  let component: PlayersComponent;
  let playerSpy: jasmine.Spy;
  let httpTestingController: HttpTestingController;

  beforeEach(() =>
  {
    TestBed.configureTestingModule({
      imports: [ HttpClientTestingModule ],
      providers: [PlayersComponent]
    });

    httpTestingController = TestBed.get(HttpTestingController);
  }
  );
  
  it('Should create players component', () => {
    const component: PlayersComponent = TestBed.get(PlayersComponent);
    expect(component).toBeTruthy();
  });

  it('Match names with IDs', () => {
    const component: PlayersComponent = TestBed.get(PlayersComponent);
    expect(component.getPlayerName(1)).toEqual("Fred");
  });

  it('Get player should be called', () => {
    const component: PlayersComponent = TestBed.get(PlayersComponent);
    playerSpy = spyOn(component, 'getPlayers'); 
    component.ngOnInit();
    expect(playerSpy).toHaveBeenCalled();
  })

  it('Test Filtering', () => {
    const component: PlayersComponent = TestBed.get(PlayersComponent);

    component.myFilterP1 = 'b';
    component.myFilterP2 = 'R';
    component.filterPlayers();
    expect(component.filtered_players_p1.length).toEqual(0);
    expect(component.filtered_players_p2.length).toEqual(1);

    component.myFilterP1 = '';
    component.myFilterP2 = '';
    component.updatePlayers([{id: 1, name: 'George'}, {id: 2, name: 'Ben'}]);
    expect(component.getPlayerName(1)).toEqual("George");
    expect(component.getPlayerName(2)).toEqual("Ben");
    expect(component.getPlayerName(3)).toEqual("");
    expect(component.filtered_players_p1).toEqual(component.players);
    expect(component.filtered_players_p2).toEqual(component.players);

    component.myFilterP1 = 'ge';
    component.myFilterP2 = 'E';
    component.filterPlayers();
    expect(component.filtered_players_p1.length).toEqual(1);
    expect(component.filtered_players_p2.length).toEqual(2);
  })

  it('Predictions', () => {
    const component: PlayersComponent = TestBed.get(PlayersComponent);
    const testData = [{title: 'Test prediction', line1: '100'}]
    expect(component.loading == false);
    component.statistic = 'Dummy';
    component.firstInput = 4;
    component.secondInput = 8;
    component.getPredictions();
    expect(component.loading == true)

    const req = httpTestingController.expectOne('http://localhost:8080/api/predictions?prediction=ALL&p1=4&p2=8');
    expect(req.request.method).toEqual('GET');
    req.flush(testData);

    expect(component.loading == false)
    expect(component.statistic.line1 == '100');
  });


});
