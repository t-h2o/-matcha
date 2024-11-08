import { Routes } from '@angular/router';
import { AuthGuard } from './auth.guard';
import { BrowsingComponent } from './browsing/browsing.component';
import { GuestGuard } from './guest.guard';
import { LoginComponent } from './login/login.component';
import { ProfileComponent } from './profile/profile.component';
import { RegisterComponent } from './register/register.component';
import { ResetPasswordComponent } from './reset-password/reset-password.component';
import { ErrorPageComponent } from './error-page/error-page.component';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  {
    path: 'login',
    component: LoginComponent,
    canActivate: [GuestGuard],
  },
  {
    path: 'profile',
    component: ProfileComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'register',
    component: RegisterComponent,
  },
  {
    path: 'browsing',
    component: BrowsingComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'reset-password',
    component: ResetPasswordComponent,
  },
  {
    path: '**',
    component: ErrorPageComponent,
  },
];
