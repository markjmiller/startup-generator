import { of, Observable } from 'rxjs';
import { flatMap, map, take } from 'rxjs/operators';
import { WordShuffler, Suggestion, GetSuggestion } from './suggestion.service';

class getSuggestion implements GetSuggestion {
    
    private index = 0;

    constructor(private suggestions: Suggestion[]) { }

    get(): Observable<Suggestion> {
        return new Observable<Suggestion>(subscriber => {
            subscriber.next(this.suggestions[this.index++]);
        }).pipe(take(1));
    }
}

function valueExpect(getSuggestion: Observable<Suggestion>, done: DoneFn, values: Suggestion[]): void {
    let resultCount = 0;
    of(...values).pipe(
        flatMap(value =>
            getSuggestion.pipe(map(expected => <any>{ value: value, expected: expected}))
        )
    )
    .forEach(x => {
        resultCount++;
        expect(x.value).toEqual(x.expected);
    })
    .then(() => {
        expect(resultCount).toBeGreaterThan(0);
        done();
    });
}

describe('WordShuffler', () => {

    const repeat = <Suggestion>{ word_1: 'A', word_2: '1'};
    const halfRepeat = <Suggestion>{ word_1: 'A', word_2: '2'};
    const newSuggestion = <Suggestion>{ word_1: 'B', word_2: '2'};

    it('does not repeat', (done: DoneFn) => {
        const suggestionsArray = [
            repeat,        /* expected */
            repeat,
            repeat,
            newSuggestion  /* expected */
        ];
        
        const shuffler = new WordShuffler(new getSuggestion(suggestionsArray), 2, 99);

        valueExpect(shuffler.get(), done, [repeat, newSuggestion]);
    });

    it('repeats after limit', (done: DoneFn) => {
        const suggestionsArray = [
            repeat,        /* expected */
            repeat,
            repeat,
            repeat,        /* expected */
            newSuggestion  /* expected */
        ];

        const shuffler = new WordShuffler(new getSuggestion(suggestionsArray), 2, 99);

        valueExpect(shuffler.get(), done, [repeat, repeat, newSuggestion]);
    });

    it('repeats after max tries', (done: DoneFn) => {
        const suggestionsArray = [
            repeat,        /* expected */
            repeat,
            repeat,        /* expected */
            repeat,
            repeat,        /* expected */
            newSuggestion  /* expected */
        ];

        const shuffler = new WordShuffler(new getSuggestion(suggestionsArray), 99, 2);

        valueExpect(shuffler.get(), done, [repeat, repeat, repeat, newSuggestion]);
    });
});
