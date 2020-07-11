/**
 * @constructor (callback, interval)
 * @brief Definition of the DynamicInterval class. Allows for intervals to be turned on and off at will.
 * @Note The interval defaults to inactive. activate_interval() must be called to activate it.
 * @param {CallableFunction} callback The function to be called after every interval
 * @param {Number} interval The period (in milliseconds) between execution of the function callback
 */
export class DynamicInterval {
    constructor(callback, interval) {
        this._callback = callback;
        this._interval_period = interval;

        // Will eventually store the created interval
        this._interval = null;
    }

    /**
     * @brief function to recereate the interval when asked
     */
    activate_interval(){
        // this._interval = setInterval(() => this._callback, this._interval_period);
        this._interval = setInterval(this._callback, this._interval_period);
    }

    deactivate_interval(){
        clearInterval(this._interval);
        this._interval = null;
    }
    
}