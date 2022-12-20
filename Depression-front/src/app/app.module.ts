import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { environment } from '@env/environment';

/* MATERIAL */
import {    MatIconModule    } from '@angular/material/icon'
import {   MatRadioModule    } from '@angular/material/radio'
import {   MatButtonModule   } from '@angular/material/button';
import {   MatInputModule    } from '@angular/material/input';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import {   MAT_DATE_LOCALE   } from '@angular/material/core';
import {   MatDividerModule  } from '@angular/material/divider';


/*SERVICES*/
import {AuthenticationService} from './_services'
import {ScoringService } from  './_services'

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NotFoundComponent } from './common/not-found/not-found.component';
import { HeaderComponent } from './common/header/header.component';
import { HomeComponent } from './common/home/home.component';

@NgModule({
  declarations: [
    AppComponent,
    NotFoundComponent,
    HeaderComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    // BrowserModule.withServerTransition({ appId: 'ng-cli-universal' }),
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    MatIconModule,
    MatButtonModule,
    MatInputModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatDividerModule,
    MatRadioModule,
  ],
  providers: [
    AuthenticationService,
    ScoringService,
    { provide: MAT_DATE_LOCALE, useValue: 'ru-Ru' },
    { provide: 'BASE_URL', useValue: environment.apiRoot }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
