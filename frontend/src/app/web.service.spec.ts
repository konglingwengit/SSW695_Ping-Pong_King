import { ComponentFixtureAutoDetect, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { WebService } from './web.service';
import { AppModule } from './app.module';

describe('WebService', () => {
  let service: WebService;
  beforeEach(() => TestBed.configureTestingModule({
    imports: [ HttpClientTestingModule],
    providers: [WebService]
  }));

  it('should be created', () => {
    
    const service: WebService = TestBed.get(WebService);
    expect(service).toBeTruthy();
  });

  it('should create', () => {
    ComponentFixtureAutoDetect
    const component: WebService = TestBed.get(WebService);
    expect(component.getIndividualStatistics(1).subscribe(result => expect(result.length).toBeGreaterThan(0)));
  });

  it('should create', () => {
    ComponentFixtureAutoDetect
    const component: WebService = TestBed.get(WebService);
    expect(component.getMatchStatistics(1,2).subscribe(result => expect(result.length).toBeGreaterThan(0)));
  });

  it('should create', () => {
    ComponentFixtureAutoDetect
    const component: WebService = TestBed.get(WebService);
    expect(component.getPredictions(1,2,'prediction').subscribe(result => expect(result.length).toBeGreaterThan(0)));
  });

  it('should create', () => {
    ComponentFixtureAutoDetect
    const component: WebService = TestBed.get(WebService);
    expect(component.getPlayers().subscribe(result => expect(result.length).toBeGreaterThan(0)));
  });

});
