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
    /**
     *
     */
    constructor(
    ) { }

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
                return value;
            }),
            catchError(err => {
                console.log(err);
                return throwError(err);
            })
        );
    }
}