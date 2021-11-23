import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';

import { PlayersComponent } from './players.component';

describe('PlayersComponent', () => {
  let component: PlayersComponent;
  //let fixture: ComponentFixture<PlayersComponent>;

  beforeEach(() => 
  TestBed.configureTestingModule({
    imports: [ HttpClientTestingModule ],
    providers: [PlayersComponent]
  }));
  /*beforeEach(() => {
    fixture = TestBed.createComponent(PlayersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });*/

  it('should create', () => {
    const component: PlayersComponent = TestBed.get(PlayersComponent);
    expect(component).toBeTruthy();
  });

  it('should return Fred', () => {
    const component: PlayersComponent = TestBed.get(PlayersComponent);
    expect(component.getPlayerName(1)).toEqual("Fred");
  });

  it('get player should be called', () => {
    const component: PlayersComponent = TestBed.get(PlayersComponent);
    spyOn(component, 'getPlayers'); 
    component.ngOnInit();
    expect(component.getPlayers()).toHaveBeenCalled();
  })
});
