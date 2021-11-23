import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { StatisticsComponent } from './statistics.component';

describe('StatisticsComponent', () => {
  let component: StatisticsComponent;
  //let fixture: ComponentFixture<StatisticsComponent>;

  beforeEach(() => 
    TestBed.configureTestingModule({
      imports: [ HttpClientTestingModule ],
      providers: [StatisticsComponent]
    }));

  /*beforeEach(() => {
    fixture = TestBed.createComponent(StatisticsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });*/

  it('should create', () => {
    const component: StatisticsComponent = TestBed.get(StatisticsComponent);
    expect(component).toBeTruthy();
  });

  it('should create', () => {
    const component: StatisticsComponent = TestBed.get(StatisticsComponent);
    expect(component.getPlayerName(1)).toEqual("Fred");
  });
  
});
