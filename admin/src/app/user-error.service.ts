import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserErrorService {

  private _userError: Subject<string> = new Subject();

  constructor() { }

  get error(): Observable<string> {
    return this._userError;
  }

  show(message: string) {
    console.log(message);
    this._userError.next(message);
  }
}
