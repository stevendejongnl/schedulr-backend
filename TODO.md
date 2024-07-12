# TODO List

## Setup and Initial Configuration
- [ ] Configure a PostgreSQL/MongoDB database for storing project data.

## API Development

### User Authentication and Authorization
- [ ] Create user registration and login endpoints.
- [ ] Implement JWT-based authentication.
- [ ] Set up permissions for different types of users (e.g., admin, user).

### Project Management
- [ ] Design and implement the project model.
- [ ] Create endpoints for creating, listing, updating, and deleting projects.
- [ ] Implement project ownership and ensure users can only access their projects.

### Planning Management within Projects
- [ ] Design and implement the planning model associated with projects.
- [ ] Create endpoints for adding, listing, updating, and deleting plannings within a project.
- [ ] Ensure that plannings can only be managed by the owner of the project.

### Planning Items Management
- [ ] Design and implement the planning item model associated with plannings.
- [ ] Create endpoints for adding, listing, updating, and deleting planning items within a planning.
- [ ] Implement sorting and filtering capabilities for planning items.

## Testing
- [x] Set up continuous integration with GitHub Actions to run tests on push.

## Documentation
- [ ] Document the API endpoints with Swagger or another API documentation tool.

## Additional Features and Improvements
- [ ] Implement rate limiting for the API.
- [ ] Add logging and monitoring with tools like Sentry.
