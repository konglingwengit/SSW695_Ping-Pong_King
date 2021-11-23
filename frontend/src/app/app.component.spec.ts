import { TestBed } from '@angular/core/testing';
import { FormsModule, FormBuilder, FormGroup,ReactiveFormsModule } from '@angular/forms';
import { HttpClientTestingModule } from '@angular/common/http/testing';

import { SocialAuthService, GoogleLoginProvider, SocialUser } from 'angularx-social-login';
import { AppComponent } from './app.component';
import { AppModule } from './app.module';

describe('AppComponent', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [ HttpClientTestingModule ,ReactiveFormsModule],
    providers: [AppComponent,SocialAuthService,GoogleLoginProvider,SocialUser]
  }));

  it('should create the app', () => {
    const component: AppComponent = TestBed.get(AppComponent);
    expect(component).toBeTruthy();
  });

  it('should create the app', () => {
    const component: AppComponent = TestBed.get(AppComponent);
    component.activateStatistics();
    expect(component.predictionsActive).toEqual(false);
    expect(component.statisticsActive).toEqual(true);
  });
  
  it('should create the app', () => {
    const component: AppComponent = TestBed.get(AppComponent);
    component.activatePredictions();
    expect(component.predictionsActive).toEqual(true);
    expect(component.statisticsActive).toEqual(false);
  });  

/*  it(`should have as title 'jms-ping-pong-proto'`, () => {
    const component: AppComponent = TestBed.get(AppComponent);
    expect(component.title).toContain('Ping Pong King');
  });

  it('should render title', () => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('.content span')?.textContent).toContain('jms-ping-pong-proto app is running!');
  });*/
});
