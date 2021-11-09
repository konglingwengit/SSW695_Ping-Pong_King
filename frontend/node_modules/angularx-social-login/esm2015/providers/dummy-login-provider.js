import { BaseLoginProvider } from '../entities/base-login-provider';
// Simulates login / logout without actually requiring an Internet connection.
//
// Useful for certain development situations.
//
// For example, if you want to simulate the greatest football referee England has ever produced:
//
//  const dummyUser: SocialUser = {
//     id: '0123456789',
//     name: 'Howard Webb',
//     email: 'howard@webb.com',
//     firstName: 'Howard',
//     lastName: 'Webb',
//     authToken: 'dummyAuthToken',
//     photoUrl: 'https://en.wikipedia.org/wiki/Howard_Webb#/media/File:Howard_Webb_march11.jpg',
//     provider: 'DUMMY',
//     idToken: 'dummyIdToken',
//     authorizationCode: 'dummyAuthCode'
// };
//
//  let config = new AuthServiceConfig([
//  { ... },
//  {
//       id: DummyLoginProvider.PROVIDER_ID,
//       provider: new DummyLoginProvider(dummyUser)  // Pass your user into the constructor
//   },
//  { ... }
//  ]);
export class DummyLoginProvider extends BaseLoginProvider {
    constructor(dummy) {
        super();
        if (dummy) {
            this.dummy = dummy;
        }
        else {
            this.dummy = DummyLoginProvider.DEFAULT_USER;
        }
        // Start not logged in
        this.loggedIn = false;
    }
    getLoginStatus() {
        return new Promise((resolve, reject) => {
            if (this.loggedIn) {
                resolve(this.dummy);
            }
            else {
                reject('No user is currently logged in.');
            }
        });
    }
    initialize() {
        return new Promise((resolve, reject) => {
            resolve();
        });
    }
    signIn() {
        return new Promise((resolve, reject) => {
            this.loggedIn = true;
            resolve(this.dummy);
        });
    }
    signOut(revoke) {
        return new Promise((resolve, reject) => {
            this.loggedIn = false;
            resolve();
        });
    }
}
DummyLoginProvider.PROVIDER_ID = 'DUMMY';
DummyLoginProvider.DEFAULT_USER = {
    id: '1234567890',
    name: 'Mickey Mouse',
    email: 'mickey@mouse.com',
    firstName: 'Mickey',
    lastName: 'Mouse',
    authToken: 'dummyAuthToken',
    photoUrl: 'https://en.wikipedia.org/wiki/File:Mickey_Mouse.png',
    provider: 'DUMMY',
    idToken: 'dummyIdToken',
    authorizationCode: 'dummyAuthCode',
    response: {},
};
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZHVtbXktbG9naW4tcHJvdmlkZXIuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi8uLi8uLi8uLi9wcm9qZWN0cy9saWIvc3JjL3Byb3ZpZGVycy9kdW1teS1sb2dpbi1wcm92aWRlci50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQSxPQUFPLEVBQUUsaUJBQWlCLEVBQUUsTUFBTSxpQ0FBaUMsQ0FBQztBQUdwRSw4RUFBOEU7QUFDOUUsRUFBRTtBQUNGLDZDQUE2QztBQUM3QyxFQUFFO0FBQ0YsZ0dBQWdHO0FBQ2hHLEVBQUU7QUFDRixtQ0FBbUM7QUFDbkMsd0JBQXdCO0FBQ3hCLDJCQUEyQjtBQUMzQixnQ0FBZ0M7QUFDaEMsMkJBQTJCO0FBQzNCLHdCQUF3QjtBQUN4QixtQ0FBbUM7QUFDbkMsaUdBQWlHO0FBQ2pHLHlCQUF5QjtBQUN6QiwrQkFBK0I7QUFDL0IseUNBQXlDO0FBQ3pDLEtBQUs7QUFDTCxFQUFFO0FBQ0Ysd0NBQXdDO0FBQ3hDLFlBQVk7QUFDWixLQUFLO0FBQ0wsNENBQTRDO0FBQzVDLDRGQUE0RjtBQUM1RixPQUFPO0FBQ1AsV0FBVztBQUNYLE9BQU87QUFFUCxNQUFNLE9BQU8sa0JBQW1CLFNBQVEsaUJBQWlCO0lBcUJ2RCxZQUFZLEtBQWtCO1FBQzVCLEtBQUssRUFBRSxDQUFDO1FBQ1IsSUFBSSxLQUFLLEVBQUU7WUFDVCxJQUFJLENBQUMsS0FBSyxHQUFHLEtBQUssQ0FBQztTQUNwQjthQUFNO1lBQ0wsSUFBSSxDQUFDLEtBQUssR0FBRyxrQkFBa0IsQ0FBQyxZQUFZLENBQUM7U0FDOUM7UUFFRCxzQkFBc0I7UUFDdEIsSUFBSSxDQUFDLFFBQVEsR0FBRyxLQUFLLENBQUM7SUFDeEIsQ0FBQztJQUVELGNBQWM7UUFDWixPQUFPLElBQUksT0FBTyxDQUFDLENBQUMsT0FBTyxFQUFFLE1BQU0sRUFBRSxFQUFFO1lBQ3JDLElBQUksSUFBSSxDQUFDLFFBQVEsRUFBRTtnQkFDakIsT0FBTyxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsQ0FBQzthQUNyQjtpQkFBTTtnQkFDTCxNQUFNLENBQUMsaUNBQWlDLENBQUMsQ0FBQzthQUMzQztRQUNILENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQUVELFVBQVU7UUFDUixPQUFPLElBQUksT0FBTyxDQUFDLENBQUMsT0FBTyxFQUFFLE1BQU0sRUFBRSxFQUFFO1lBQ3JDLE9BQU8sRUFBRSxDQUFDO1FBQ1osQ0FBQyxDQUFDLENBQUM7SUFDTCxDQUFDO0lBRUQsTUFBTTtRQUNKLE9BQU8sSUFBSSxPQUFPLENBQUMsQ0FBQyxPQUFPLEVBQUUsTUFBTSxFQUFFLEVBQUU7WUFDckMsSUFBSSxDQUFDLFFBQVEsR0FBRyxJQUFJLENBQUM7WUFDckIsT0FBTyxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsQ0FBQztRQUN0QixDQUFDLENBQUMsQ0FBQztJQUNMLENBQUM7SUFFRCxPQUFPLENBQUMsTUFBZ0I7UUFDdEIsT0FBTyxJQUFJLE9BQU8sQ0FBQyxDQUFDLE9BQU8sRUFBRSxNQUFNLEVBQUUsRUFBRTtZQUNyQyxJQUFJLENBQUMsUUFBUSxHQUFHLEtBQUssQ0FBQztZQUN0QixPQUFPLEVBQUUsQ0FBQztRQUNaLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQzs7QUE1RHNCLDhCQUFXLEdBQVcsT0FBTyxDQUFDO0FBRXJDLCtCQUFZLEdBQUc7SUFDN0IsRUFBRSxFQUFFLFlBQVk7SUFDaEIsSUFBSSxFQUFFLGNBQWM7SUFDcEIsS0FBSyxFQUFFLGtCQUFrQjtJQUN6QixTQUFTLEVBQUUsUUFBUTtJQUNuQixRQUFRLEVBQUUsT0FBTztJQUNqQixTQUFTLEVBQUUsZ0JBQWdCO0lBQzNCLFFBQVEsRUFBRSxxREFBcUQ7SUFDL0QsUUFBUSxFQUFFLE9BQU87SUFDakIsT0FBTyxFQUFFLGNBQWM7SUFDdkIsaUJBQWlCLEVBQUUsZUFBZTtJQUNsQyxRQUFRLEVBQUUsRUFBRTtDQUNiLENBQUMiLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgeyBCYXNlTG9naW5Qcm92aWRlciB9IGZyb20gJy4uL2VudGl0aWVzL2Jhc2UtbG9naW4tcHJvdmlkZXInO1xuaW1wb3J0IHsgU29jaWFsVXNlciB9IGZyb20gJy4uL2VudGl0aWVzL3NvY2lhbC11c2VyJztcblxuLy8gU2ltdWxhdGVzIGxvZ2luIC8gbG9nb3V0IHdpdGhvdXQgYWN0dWFsbHkgcmVxdWlyaW5nIGFuIEludGVybmV0IGNvbm5lY3Rpb24uXG4vL1xuLy8gVXNlZnVsIGZvciBjZXJ0YWluIGRldmVsb3BtZW50IHNpdHVhdGlvbnMuXG4vL1xuLy8gRm9yIGV4YW1wbGUsIGlmIHlvdSB3YW50IHRvIHNpbXVsYXRlIHRoZSBncmVhdGVzdCBmb290YmFsbCByZWZlcmVlIEVuZ2xhbmQgaGFzIGV2ZXIgcHJvZHVjZWQ6XG4vL1xuLy8gIGNvbnN0IGR1bW15VXNlcjogU29jaWFsVXNlciA9IHtcbi8vICAgICBpZDogJzAxMjM0NTY3ODknLFxuLy8gICAgIG5hbWU6ICdIb3dhcmQgV2ViYicsXG4vLyAgICAgZW1haWw6ICdob3dhcmRAd2ViYi5jb20nLFxuLy8gICAgIGZpcnN0TmFtZTogJ0hvd2FyZCcsXG4vLyAgICAgbGFzdE5hbWU6ICdXZWJiJyxcbi8vICAgICBhdXRoVG9rZW46ICdkdW1teUF1dGhUb2tlbicsXG4vLyAgICAgcGhvdG9Vcmw6ICdodHRwczovL2VuLndpa2lwZWRpYS5vcmcvd2lraS9Ib3dhcmRfV2ViYiMvbWVkaWEvRmlsZTpIb3dhcmRfV2ViYl9tYXJjaDExLmpwZycsXG4vLyAgICAgcHJvdmlkZXI6ICdEVU1NWScsXG4vLyAgICAgaWRUb2tlbjogJ2R1bW15SWRUb2tlbicsXG4vLyAgICAgYXV0aG9yaXphdGlvbkNvZGU6ICdkdW1teUF1dGhDb2RlJ1xuLy8gfTtcbi8vXG4vLyAgbGV0IGNvbmZpZyA9IG5ldyBBdXRoU2VydmljZUNvbmZpZyhbXG4vLyAgeyAuLi4gfSxcbi8vICB7XG4vLyAgICAgICBpZDogRHVtbXlMb2dpblByb3ZpZGVyLlBST1ZJREVSX0lELFxuLy8gICAgICAgcHJvdmlkZXI6IG5ldyBEdW1teUxvZ2luUHJvdmlkZXIoZHVtbXlVc2VyKSAgLy8gUGFzcyB5b3VyIHVzZXIgaW50byB0aGUgY29uc3RydWN0b3Jcbi8vICAgfSxcbi8vICB7IC4uLiB9XG4vLyAgXSk7XG5cbmV4cG9ydCBjbGFzcyBEdW1teUxvZ2luUHJvdmlkZXIgZXh0ZW5kcyBCYXNlTG9naW5Qcm92aWRlciB7XG4gIHB1YmxpYyBzdGF0aWMgcmVhZG9ubHkgUFJPVklERVJfSUQ6IHN0cmluZyA9ICdEVU1NWSc7XG5cbiAgc3RhdGljIHJlYWRvbmx5IERFRkFVTFRfVVNFUiA9IHtcbiAgICBpZDogJzEyMzQ1Njc4OTAnLFxuICAgIG5hbWU6ICdNaWNrZXkgTW91c2UnLFxuICAgIGVtYWlsOiAnbWlja2V5QG1vdXNlLmNvbScsXG4gICAgZmlyc3ROYW1lOiAnTWlja2V5JyxcbiAgICBsYXN0TmFtZTogJ01vdXNlJyxcbiAgICBhdXRoVG9rZW46ICdkdW1teUF1dGhUb2tlbicsXG4gICAgcGhvdG9Vcmw6ICdodHRwczovL2VuLndpa2lwZWRpYS5vcmcvd2lraS9GaWxlOk1pY2tleV9Nb3VzZS5wbmcnLFxuICAgIHByb3ZpZGVyOiAnRFVNTVknLFxuICAgIGlkVG9rZW46ICdkdW1teUlkVG9rZW4nLFxuICAgIGF1dGhvcml6YXRpb25Db2RlOiAnZHVtbXlBdXRoQ29kZScsXG4gICAgcmVzcG9uc2U6IHt9LFxuICB9O1xuXG4gIHByaXZhdGUgZHVtbXk6IFNvY2lhbFVzZXI7XG5cbiAgcHJpdmF0ZSBsb2dnZWRJbjogYm9vbGVhbjtcblxuICBjb25zdHJ1Y3RvcihkdW1teT86IFNvY2lhbFVzZXIpIHtcbiAgICBzdXBlcigpO1xuICAgIGlmIChkdW1teSkge1xuICAgICAgdGhpcy5kdW1teSA9IGR1bW15O1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLmR1bW15ID0gRHVtbXlMb2dpblByb3ZpZGVyLkRFRkFVTFRfVVNFUjtcbiAgICB9XG5cbiAgICAvLyBTdGFydCBub3QgbG9nZ2VkIGluXG4gICAgdGhpcy5sb2dnZWRJbiA9IGZhbHNlO1xuICB9XG5cbiAgZ2V0TG9naW5TdGF0dXMoKTogUHJvbWlzZTxTb2NpYWxVc2VyPiB7XG4gICAgcmV0dXJuIG5ldyBQcm9taXNlKChyZXNvbHZlLCByZWplY3QpID0+IHtcbiAgICAgIGlmICh0aGlzLmxvZ2dlZEluKSB7XG4gICAgICAgIHJlc29sdmUodGhpcy5kdW1teSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICByZWplY3QoJ05vIHVzZXIgaXMgY3VycmVudGx5IGxvZ2dlZCBpbi4nKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfVxuXG4gIGluaXRpYWxpemUoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgcmV0dXJuIG5ldyBQcm9taXNlKChyZXNvbHZlLCByZWplY3QpID0+IHtcbiAgICAgIHJlc29sdmUoKTtcbiAgICB9KTtcbiAgfVxuXG4gIHNpZ25JbigpOiBQcm9taXNlPFNvY2lhbFVzZXI+IHtcbiAgICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUsIHJlamVjdCkgPT4ge1xuICAgICAgdGhpcy5sb2dnZWRJbiA9IHRydWU7XG4gICAgICByZXNvbHZlKHRoaXMuZHVtbXkpO1xuICAgIH0pO1xuICB9XG5cbiAgc2lnbk91dChyZXZva2U/OiBib29sZWFuKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgcmV0dXJuIG5ldyBQcm9taXNlKChyZXNvbHZlLCByZWplY3QpID0+IHtcbiAgICAgIHRoaXMubG9nZ2VkSW4gPSBmYWxzZTtcbiAgICAgIHJlc29sdmUoKTtcbiAgICB9KTtcbiAgfVxufVxuIl19