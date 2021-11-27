import { TestBed } from '@angular/core/testing';
import { FormsModule, FormBuilder, FormGroup,ReactiveFormsModule } from '@angular/forms';
import { HttpClientTestingModule } from '@angular/common/http/testing';

import { SocialAuthService, GoogleLoginProvider, SocialUser } from 'angularx-social-login';
import { AppComponent } from './app.component';
import { AppModule } from './app.module';

describe('AppComponent', () => {
  let authSpy: jasmine.Spy;
  let googleLoginProviderSpy: jasmine.Spy;

  beforeEach(() =>
  {
    authSpy = jasmine.createSpyObj('SocialAuthService', ['authState', 'signIn', 'signOut']);
    googleLoginProviderSpy = jasmine.createSpyObj('GoogleLoginProvider', ['PROVIDER_ID']);
    TestBed.configureTestingModule(
    {
      imports: [ HttpClientTestingModule ,ReactiveFormsModule],
      providers: [AppComponent,{provide: SocialAuthService, useValue: authSpy},{provide: GoogleLoginProvider, useValue: googleLoginProviderSpy},SocialUser]
    });
  }
  );

  it('should create the app', () => {
    const component: AppComponent = TestBed.get(AppComponent);
    expect(component).toBeTruthy();
  });

  it('Switch to statistics', () => {
    const component: AppComponent = TestBed.get(AppComponent);
    component.activateStatistics();
    expect(component.predictionsActive).toEqual(false);
    expect(component.statisticsActive).toEqual(true);
  });
  
  it('Switch to predictions', () => {
    const component: AppComponent = TestBed.get(AppComponent);
    component.activatePredictions();
    expect(component.predictionsActive).toEqual(true);
    expect(component.statisticsActive).toEqual(false);
  });  

});
