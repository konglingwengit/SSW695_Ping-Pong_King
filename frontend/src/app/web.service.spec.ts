import { ComponentFixtureAutoDetect, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { WebService } from './web.service';
import { AppModule } from './app.module';

describe('WebService', () => {
  let service: WebService;
  let httpTestingController: HttpTestingController;
  beforeEach(() =>
  {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [WebService]
    });

    httpTestingController = TestBed.get(HttpTestingController);
    service = TestBed.get(WebService);
  });

  afterEach(() =>
  {
    httpTestingController.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('Individual Stats', () => {
    ComponentFixtureAutoDetect
    const testString = 'Testing ind'
    expect(service.getIndividualStatistics(1).subscribe(result => expect(result).toEqual(testString)));

    const req = httpTestingController.expectOne('http://localhost:8080/api/single_player_stats?p1=1');
    expect(req.request.method).toEqual('GET');
    req.flush(testString);
  });

  it('Vs Stats', () => {
    ComponentFixtureAutoDetect
    const testString = 'Testing vs'
    expect(service.getMatchStatistics(1,2).subscribe(result => expect(result).toEqual(testString)));

    const req = httpTestingController.expectOne('http://localhost:8080/api/vs_stats?p1=1&p2=2');
    expect(req.request.method).toEqual('GET');
    req.flush(testString);
  });

  it('Predictions', () => {
    ComponentFixtureAutoDetect
    const testString = 'Testing pred'
    expect(service.getPredictions(1,2,'ALL').subscribe(result => expect(result).toEqual(testString)));

    const req = httpTestingController.expectOne('http://localhost:8080/api/predictions?prediction=ALL&p1=1&p2=2');
    expect(req.request.method).toEqual('GET');
    req.flush(testString);
  });

  it('Get Players Response', () => {
    let retrievedPlayers: any;
    const mockPlayers =
    [
      {
        name: 'John',
        id: 7
      },
      {
        name: 'Mark',
        id: 8
      }
    ];
    expect(service.getPlayers().subscribe(result => retrievedPlayers = result));

    const req = httpTestingController.expectOne('http://localhost:8080/api/players');
    expect(req.request.method).toEqual('GET');
    req.flush(mockPlayers);

    expect(retrievedPlayers).toEqual(mockPlayers);
    
  });

});
