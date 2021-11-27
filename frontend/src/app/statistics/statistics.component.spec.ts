import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import { StatisticsComponent } from './statistics.component';

describe('StatisticsComponent', () => {
  let component: StatisticsComponent;
  let playerSpy: jasmine.Spy;
  let httpTestingController: HttpTestingController;

  beforeEach(() =>
  {

    TestBed.configureTestingModule({
      imports: [ HttpClientTestingModule ],
      providers: [StatisticsComponent]
    });

    httpTestingController = TestBed.get(HttpTestingController);
  }
  );

  it('Should create statistics component', () => {
    const component: StatisticsComponent = TestBed.get(StatisticsComponent);
    expect(component).toBeTruthy();
  });

  it('Match names with IDs', () => {
    const component: StatisticsComponent = TestBed.get(StatisticsComponent);
    expect(component.getPlayerName(1)).toEqual("Fred");
  });

  it('Get player should be called', () => {
    const component: StatisticsComponent = TestBed.get(StatisticsComponent);
    playerSpy = spyOn(component, 'getPlayers'); 
    component.ngOnInit();
    expect(playerSpy).toHaveBeenCalled();
  })

  it('Test Filtering', () => {
    const component: StatisticsComponent = TestBed.get(StatisticsComponent);

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

  it('Individual Stats', () => {
    const component: StatisticsComponent = TestBed.get(StatisticsComponent);
    const testData = [{name: 'Test statistic', data: '100'}, {name: 'Another', data: '20'}]
    expect(component.loading == false);
    component.statistic = 'Dummy';
    component.vs_statistic = 'Dummy';
    component.getPlayerStatistics(1);
    expect(component.loading == true)
    expect(component.statistic.length).toEqual(0);
    expect(component.vs_statistic.length).toEqual(0);

    const req = httpTestingController.expectOne('http://localhost:8080/api/single_player_stats?p1=1');
    expect(req.request.method).toEqual('GET');
    req.flush(testData);

    expect(component.loading == false)
    expect(component.statistic.data == '100');
    expect(component.vs_statistic.length).toEqual(0);
  });

  it('Matchup Stats', () => {
    const component: StatisticsComponent = TestBed.get(StatisticsComponent);
    const testData = [{name: 'Test statistic', data: '100'}, {name: 'Another', data: '20'}]
    expect(component.loading == false);
    component.statistic = 'Dummy';
    component.vs_statistic = 'Dummy';
    component.getVsStatistics(1, 2);
    expect(component.loading == true)
    expect(component.statistic.length).toEqual(0);
    expect(component.vs_statistic.length).toEqual(0);

    const req = httpTestingController.expectOne('http://localhost:8080/api/vs_stats?p1=1&p2=2');
    expect(req.request.method).toEqual('GET');
    req.flush(testData);

    expect(component.loading == false)
    expect(component.statistic.length).toEqual(0);
    expect(component.vs_statistic.data == '100');
  });

});
