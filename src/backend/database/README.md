# Purpose of files in this folder
* The databse choosen is mongoDB. Interfacing that with python requires pymongo.
* Classes that interface between pymongo's API and the rest of the backend codebase
    * Provide common utility/usage functions to reduce code that is re-used/copy+paste
* Allows the program to store sensitive information in databases rather than regialr .txt or .json files

## Hierarchy of the Database
* Every collection (currently plan on 1 or 2) goes through an overarching collection manager
* Each collection gets its own class representing how it interacts/interfaces with the rest of the program + mongodb
* The only currently garunteed collection is the `users` collection
* `users` will contain login/registration information about each user
    * Each card of the collection contains the following:
        * Serialized copy of their `User` object  of the class `WebAppUser`. It contains:
            1. `username`
            2. `password`
            3. `id` (really a UUID for each user)
            4. `backend_controller` (an object of the entire backend code)
* Another potential collection might be `user_results` that will store timing data for any given user
    * The structure would be the same as the `store_results` folder and `_task_json` in time_manager.py
    * It would be keyed/unique to each user also stored in the `users`
    * Useful for reducing space taken up/visible in the codebase itself 


