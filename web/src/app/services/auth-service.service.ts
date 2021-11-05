import { Injectable } from "@angular/core";
import { from, Observable, throwError } from 'rxjs'
import { map, catchError } from 'rxjs/operators';
import {
    getAuth,
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    UserCredential
} from 'firebase/auth';

/**
 * Handles authentication
 */
@Injectable({
    providedIn: 'root'
})
export default class AuthService {
    private _user: UserCredential | null = null;

    public get user(): UserCredential | null { return this._user; }

    /**
     *
     */
    constructor(
    ) { }

    public signInWithEMailAndPassword(email: string, password: string): Observable<UserCredential> {
        var auth = getAuth();
        var promise = signInWithEmailAndPassword(auth, email, password);
        return from(promise).pipe(
            map(value => {
                this._user = value;
                return value;
            }),
            catchError(err => {
                console.error(err);
                return throwError(err);
            })
        )
    }

    /**
     * 
     * @param email 
     * @param password 
     * @returns 
     */
    public createUserWithUsernameAndPassword(email: string, password: string): Observable<UserCredential> {
        var auth = getAuth();
        var promise = createUserWithEmailAndPassword(auth, email, password);
        return from(promise).pipe(
            map(value => {
                this._user = value;
                return value;
            }),
            catchError(err => {
                console.error(err);
                return throwError(err);
            })
        );
    }
}