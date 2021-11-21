import { Component,OnInit } from '@angular/core';
import { environment } from 'src/environments/environment';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { SocialAuthService, GoogleLoginProvider, SocialUser } from 'angularx-social-login';
import { PlayerService } from './player.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'Ping Pong King - early prototyping work';
  webapiurl = environment.webapiurl;

  loginForm: FormGroup;
  socialUser: SocialUser;
  isLoggedin: boolean = false;
  isAuthorized: boolean = false;
  loading: boolean = false;
  statisticsActive: boolean = false;
  predictionsActive: boolean = true;
  
  constructor(
    private formBuilder: FormBuilder, 
    private socialAuthService: SocialAuthService,
    private playerService: PlayerService
  ) { }

  ngOnInit() {
    // this.loginForm = this.formBuilder.group({
    //   email: ['', Validators.required],
    //   password: ['', Validators.required]
    // });    
    
    this.socialAuthService.authState.subscribe((user) => {
      if(user != null){
        this.socialUser = user;
        //console.log(this.socialUser);
        this.loading = true;
        this.playerService.checkUser(user.email)
          .subscribe(res => {
            this.loading = false;
            this.isLoggedin = true;
            if(String(res) == 'User authorized - ' + this.socialUser.email)
            {
              this.isAuthorized = true;
            }
            else
            {
              this.isAuthorized = false;
            }
            //console.log('res',res);
          });
      }
      else{
        this.isLoggedin = false;
        this.isAuthorized = false;
      }
    });
  }

  loginWithGoogle(): void {
    this.socialAuthService.signIn(GoogleLoginProvider.PROVIDER_ID);
  }

  logOut(): void {
    this.socialAuthService.signOut();
  }

  activateStatistics(): void {
    this.predictionsActive = false;
    this.statisticsActive = true;
  }

  activatePredictions(): void {
    this.statisticsActive = false;
    this.predictionsActive = true;
  }

}
