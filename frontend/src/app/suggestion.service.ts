import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from './../environments/environment';
import { Observable, of } from 'rxjs';
import { delay, map, catchError, take } from 'rxjs/operators';

export interface Suggestion {
  word_1: string;
  word_2: string;
}

export interface GetSuggestion {
  get(): Observable<Suggestion>;
}

export class WordShuffler {

  private _words = {};

  constructor(
    private getSuggestion: GetSuggestion,
    private reset_after: number,
    private max_tries: number) {  }

  private addWordFrequency(word: string) {
    if (word in this._words) {
      this._words[word] += 1;
      this._words[word] %= this.reset_after + 1;
    }
    else {
      this._words[word] = 1;
    }
  }

  private getWordFrequency(word: string) {
    if (word in this._words) {
      return this._words[word];
    }
    return 0;
  }

  public get(): Observable<Suggestion> {
    let retry = 1;
    return this.getSuggestion.get().pipe(
      take(1),
      map(suggestion => {
        const freq1 = this.getWordFrequency(suggestion.word_1);
        const freq2 = this.getWordFrequency(suggestion.word_2);

        if (freq1 > 0 || freq2 > 0)
        {
          this.addWordFrequency(suggestion.word_1);
          this.addWordFrequency(suggestion.word_2);
          throw suggestion;
        }

        this.addWordFrequency(suggestion.word_1);
        this.addWordFrequency(suggestion.word_2);

        return suggestion;
      }),
      catchError((suggestion, caught) => {
        if (!('word_1' in suggestion))
        {
          throw suggestion;  // Actually an error
        }

        retry++;
        if (retry == this.max_tries)
        {
          retry = 0;
          return of(suggestion);
        }
        return caught;  // Retries observable
      })
    )
  }
}

@Injectable({
  providedIn: 'root'
})
export class SuggestionService implements GetSuggestion {

  constructor(private http: HttpClient) { }
  
  get(): Observable<Suggestion> {
    return this.http.get<Suggestion>(environment.api).pipe(delay(environment.suggestionDelay));
  }
}
