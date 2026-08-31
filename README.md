## Project Overview

Time Capsule News is an interactive web platform designed to preserve and contrast historical perspectives by allowing users to explore how past events were perceived in real-time versus how they are interpreted with future hindsight. Unlike standard social networks or e-commerce platforms, the application centers around an evolving chronological timeline that bridges past news, public opinion, and reflective analysis. The platform provides a rich user experience featuring interactive pages for viewing current news feeds, submitting and exploring time-stamped opinions, engaging with dynamically generated quizzes, publishing posts, and managing content moderation through a reporting system. Powered by a Django backend and enhanced with custom JavaScript and responsive Bootstrap design, the app delivers dynamic asynchronous content loading, client-side interactivity, and tailored user flows without requiring full page refreshes.

------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------

# Distinctiveness and Complexity

## Feature 1: Custom Django Forms (`PostNews` and `PostOpinion`)

### Description

To handle user contributions securely and dynamically, the application uses custom Django Forms rather than relying solely on basic HTML forms. Key aspects include:

- **Dynamic Queryset Initialization:** In the `PostOpinion` form, database querysets for `labels_select` and `article` are dynamically initialized inside the form's `__init__` method (`Label.objects.all()` and `Article.objects.all()`). This ensures the form always uses the latest data.
- **Advanced UI & Input Customization:**  
  - The `article` field uses a `ModelChoiceField` overridden with a `forms.TextInput(attrs={'list': 'opinion-datalist'})` widget, enabling custom HTML `<datalist>` autocomplete functionality linked to database records.  
  - Utilizes `ModelMultipleChoiceField` rendered with `CheckboxSelectMultiple` for tag/label assignment, alongside custom radio select widgets (`RadioSelect`) for content popularity metrics (`High`, `Medium`, `Low`).  
  - The `PostNews` form enforces structured input by validating primary and optional secondary image URLs (`URLField`), source attribution URLs, and rich text content.

### Distinctiveness

This feature moves beyond standard Django form usage by actively fighting stale database caches and providing a modern, searchable interface for relational fields. Instead of showing unwieldy dropdowns for potentially thousands of related records, it combines a text input with a native datalist, preserving Django’s server-side validation while delivering a fast, type-ahead experience. The forms also handle multiple media URLs and source attributions, structuring submissions into a rich relational ecosystem rather than flat text records—a clear departure from typical CS50W form implementations.

### Complexity

- **Mitigating Stale Database Caches:** Defining querysets at the class attribute level would cause Django to evaluate the database query only once at server startup. Overriding `__init__` ensures the form queries the database on every request, guaranteeing that newly added articles or labels appear instantly without requiring a server restart.
- **Hybrid Validation & UX:** Overriding the widget of a `ModelChoiceField` to a `TextInput` linked to a frontend `<datalist>` enables a searchable user experience while retaining Django's strict model-instance validation on submission.
- **Multi-Layered Data Relations:** The forms integrate multiple distinct data types—primary and optional secondary media links, choice-based popularity metrics, tag assignments, and source attributions—structuring user submissions into a complex relational ecosystem.

---

## Feature 2: User-Aware Article View Tracking

### Description

View tracking is handled by a reusable helper function (`add_viewers(user, article_id)`) located in `utils.py`. When a user requests an article, the function records the view by adding the user instance to the article’s Many-to-Many `views` relation (`article.views.add(user)`). Because `views` is a Many-to-Many field, each user is counted only once per article.

### Distinctiveness

Unlike typical view counters that simply increment an integer, this implementation uses database-level uniqueness to provide deduplicated analytics. The logic is encapsulated in a modular helper, ensuring consistent tracking across both standard Django views and API endpoints without code duplication. This clean separation of concerns and cross-layer state synchronization sets it apart from basic analytics approaches.

### Complexity

- **Deduplicated Analytics via Relational Sets:** Using a Many-to-Many relationship with `.add(user)` leverages database constraints to prevent artificial inflation by repeated page refreshes, providing precise per-user analytics.
- **Modular Helper Architecture:** Encapsulating the logic inside `utils.py` allows any endpoint serving article data to invoke `add_viewers()` without cluttering core view logic, promoting maintainability and DRY principles.
- **Cross-Layer State Synchronization:** Because the helper is used in both standard rendering views and REST API routes, view counts remain perfectly synchronized in the database regardless of how the user accesses the content.

---

## Feature 3: Client-Side State Locking via Asynchronous Timers (“ADHD Button”)

### Description

This feature introduces an interactive “ADHD Button” built with pure JavaScript time-interval functions (`setInterval` and `clearInterval`). When activated, the button initiates a countdown timer, dynamically updates the `.value` and `.textContent` of the DOM element every second, applies visual feedback via color-shifting functions (`change_color()` and `revert_color()`), and temporarily disables surrounding UI controls (`#opinion-button` and `#random-button`) until the counter resets.

### Distinctiveness

The feature goes beyond simple event handling by implementing a client-side state machine that enforces behavioral constraints. It locks multiple UI elements for a set duration, helping users maintain focus and reduce impulsive clicking. The combination of asynchronous DOM updates, timer management, and multi-element locking creates a unique user experience tool specifically designed for content retention—something not seen in typical CS50W projects.

### Complexity

- **Asynchronous DOM State Management:** The feature manages real-time UI state entirely on the client side without server requests. Binding event listeners on `DOMContentLoaded` and managing `setInterval` timer IDs globally tracks active time states, updates text nodes every 1000ms, and cleans up with `clearInterval` to prevent memory leaks and competing timers.
- **Behavioral UI/UX Constraints:** The script dynamically mutates element attributes (disabling `#opinion-button` and `#random-button` on trigger and re-enabling them when `counter >= duration`) to enforce specific interaction patterns, controlling multi-element UI availability based on timing thresholds.
- **Building Beyond CS50W Core Material:** This implementation combines interval timing, state reset logic, visual UI toggles, and multi-button locking into a cohesive user-experience tool that extends far beyond the basic JavaScript concepts taught in the course.

---

## Feature 4: Dynamic Bias Metric Visualization and Conditional UI Rendering

### Description

The platform transforms user self-reported bias scores (integer field ranging from 0 to 100) into dynamic visual indicators across multiple UI layers. Opinion cards evaluate the `opinion.bias` value to conditionally render:

- **Categorical Badge Labels:** Maps numerical ranges into distinct behavioral categories (“Critical Thinker” for `<40`, “Reflecting” for `<70`, and “Venting” for `≥70`).
- **Contextual Color Systems:** Automatically applies conditional background colors to card titles and badges (soft green `rgb(212, 237, 218)` for low bias, soft yellow `rgb(255, 243, 205)` for medium bias, and soft red `rgb(250, 218, 221)` for high bias).
- **Proportional Bootstrap Progress Bars:** Converts numeric inputs into visual progress bars using dynamic inline width styling (`style="width: {{ opinion.bias }}%;"`) paired with matching Bootstrap background utility classes (`bg-success`, `bg-warning`, `bg-danger`).
- **State-Aware Reporting Controls:** Checks user relations (`{% if request.user in opinion.reporter.all %}`) directly within the template to conditionally render disabled “Reported” badges versus active reporting forms containing CSRF protection.

### Distinctiveness

Rather than simply displaying raw numbers, the template layer acts as an interpretive visual engine that translates a single integer into a rich, multi-dimensional user experience. It also performs authorization checks directly in the template, preventing duplicate moderation actions and swapping active forms for disabled indicators without extra database queries. This seamless integration of Django template logic with Bootstrap components creates a highly intuitive and responsive interface.

### Complexity

- **Multi-Tiered Visual Data Mapping:** The template uses threshold logic (`if/elif/else`) to synchronize three separate UI elements—title background tinting, semantic textual badging, and graphical progress bar widths—creating an intuitive visual hierarchy for user opinions.
- **Template-Level Stateful Authorization & Moderation:** Direct relational checks against Many-to-Many fields (`opinion.reporter.all`) determine on the fly whether the current user has already reported the opinion, preventing duplicate submissions on the frontend and swapping active POST forms for disabled status indicators without additional queries.
- **Seamless Integration of Django + Bootstrap:** The feature marries Django’s dynamic template tags with Bootstrap components (striped progress bars, rounded badges, flex utilities) to translate server-side model attributes directly into responsive visual components.

---

## Feature 5: Collapsible Moderation Queue with Keyframe Disappearance Animations

### Description

The moderation workspace for reported content uses expandable UI elements paired with CSS `@keyframes` animations to keep the interface uncluttered while handling reported posts:

- **Collapsible Content Toggle:** Leverages Bootstrap's collapse plugin (`data-toggle="collapse"`) with unique dynamic IDs (`#collapseOpinion{{ opinion.id }}`) so moderators can expand and inspect post content on demand.
- **Data-Attribute Element Binding:** Connects moderation controls (`Remove` and `Keep` buttons) directly to target post containers via dynamic `data-opinion-id` HTML attributes.
- **Asynchronous Removal via CSS Animation:** Uses a CSS keyframe animation (`hide`) with `animation-play-state: paused` and `animation-fill-mode: forwards`. When a moderator approves or deletes a post, JavaScript triggers the animation by unpausing `animation-play-state`, scaling down the element (`transform: scale(0.80)`), and fading its opacity (`opacity: 0.1`) before removing the node from the DOM entirely.

### Distinctiveness

This feature delivers a non-disruptive moderation workflow—reported items animate out smoothly instead of disappearing abruptly, providing clear visual feedback without breaking the moderator's scroll context or requiring full-page reloads. The use of data-attributes and dynamic collapse IDs ensures precise targeting and keeps the moderation queue dense and readable, which is a departure from typical moderation interfaces.

### Complexity

- **Non-Disruptive Dynamic Moderation Workflow:** Combining CSS keyframe transitions with asynchronous handlers allows reported items to animate out of sight smoothly, improving user experience and preserving context.
- **Attribute-Driven JavaScript Interactivity:** Embedding `data-opinion-id` across HTML wrapper blocks and action buttons allows JavaScript event listeners (from `reported-opinions.js`) to identify exactly which DOM tree branch to animate and isolate, ensuring actions do not affect surrounding elements.
- **Optimized Layout Density with Collapsible UI:** Hiding heavy post text inside dynamic Bootstrap collapses (`collapseOpinion{{ opinion.id }}`) keeps the queue dense and readable, enabling admins to quickly review metadata across many reported items at once.

---

## Feature 6: Embedded React Flip-Card Quiz Component with Asynchronous API Fetching

### Description

The project integrates a client-side React component (transpiled via Babel) directly within an HTML view:

- **Server-to-Client Initial State Bootstrapping:** Uses an inline `window.newQuiz` JavaScript global variable to inject initial Django context data (`{{ quiz.question }}` and `{{ quiz.answer }}`) into React state (`useState`) without making an unnecessary immediate API call.
- **Dynamic React State Management:** Tracks answer visibility (`myAnswer`) and active quiz content (`quiz`) using React hooks, allowing single-click state toggles between question and answer text alongside visual CSS card flip effects (`myAnswer ? 'flip' : ''`).
- **Asynchronous Fetch Pipeline (`/get/quiz/api/`):** Fetches new quiz data asynchronously on user trigger (`getNextQuiz`), updating the local state and automatically resetting the card flip state back to the question view without full-page reloads.

### Distinctiveness

This feature demonstrates a hybrid architecture that bridges Django’s server-rendered templates with a modern JavaScript library (React). Instead of choosing between a pure server-rendered page or a fully decoupled SPA, the project uses Django for initial context delivery and routing while React handles local state, event dispatching, and asynchronous API communication. This combination provides a responsive, application-like experience while preserving Django’s strengths.

### Complexity

- **Hybrid Django-React Architecture Integration:** Django handles initial context delivery and routing, while React manages component state, event dispatching, and asynchronous REST API communication—an architecture that requires careful synchronization.
- **Decoupled Asynchronous State Updates:** Routing new quiz requests through a dedicated API endpoint (`/get/quiz/api/`) decouples frontend updates from backend page renders. Fetching JSON payloads directly into component state optimizes DOM rendering performance and creates a responsive user experience.
- **Multi-Faceted Frontend Tech Stack Synergy:** The component combines JSX, Babel, React state management (`useState`), CSS card-flip keyframe transformations, dynamic class toggles, and RESTful fetch calls inside Django’s templating ecosystem—demonstrating technical breadth beyond standard CS50W vanilla JavaScript assignments.

------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------

# What’s contained in each file created.

## Template Files Overview

### `card.html`
Renders the main article display card. Includes:
- A Bootstrap carousel for article images (falls back to a placeholder if none).
- Article title, author name, and content.
- Popularity and view count badges.
- Source URL link and post creation date.
- Buttons to view opinions (`/specific_opinions`) and load a random article (`/random_post`).
- An "ADHD" toggle button that triggers client-side countdown and locks other controls.

### `create_opinion.html`
Form for authenticated users to create an opinion. Fields:
- Title, author name, and content.
- Checkbox selection for labels/tags (`labels_select`).
- Range slider for bias (0–100).
- Article selection using a text input with a `<datalist>` populated by all articles.
- Submit button to publish.

### `create_post.html`
Editor-only form for creating a main news article. Fields:
- Title, author name.
- Three URL fields for images (main required, two optional).
- Content textarea.
- Radio buttons for popularity (High/Medium/Low).
- Source URL.
- Submit button.

### `game.html`
A standalone quiz page (does not extend `layout.html`). Includes:
- Full HTML head with Bootstrap, Google Fonts, and React/Babel CDN.
- Inline React component (`App`) that displays a quiz question/answer and fetches new quizzes from `/get/quiz/api/`.
- Card flip animation toggled by state.
- No navigation; intended to be accessed directly or via link.

### `index.html`
Extends `layout.html`. Contains:
- The `card.html` include to display the latest article.
- Loads the external script `ADHD-button.js` for timer and locking behaviour.

### `layout.html`
The main base template for all pages except `game.html`. Contains:
- HTML `<head>` with Bootstrap, project stylesheet, and Google Fonts.
- Sticky navbar with links to Home, Opinions, Quiz, Create Opinion, and editor-only links (Create Post, Reported).
- User badge showing username and role (Editor/User) using conditional logic.
- Main content block (`{% block body %}`).
- Footer with jQuery and Bootstrap JS.

### `login.html`
Extends `layout.html`. Displays a simple login form with username and password fields. Shows error message if any (`message`).

### `opinions.html`
Extends `layout.html`. Lists all opinions submitted by users. Each opinion card:
- Shows title, author, content.
- Bias level badge (Critical Thinker/Reflecting/Venting) with colour coding.
- Bootstrap progress bar representing bias percentage.
- Report button that toggles to "Reported" if already reported by the current user.
- Displays related labels.

### `register.html`
Extends `layout.html`. Displays a registration form with username, password, and confirmation fields. Shows error messages if passwords don't match or username exists.

### `reported_opinions.html`
Extends `layout.html`. Editor-only view listing all reported opinions. For each reported opinion:
- Shows title, writer, and action buttons (View Content, Remove, Keep).
- Uses Bootstrap collapse to show/hide the opinion content.
- Includes `data-opinion-id` attributes for JavaScript handling.
- Loads external script `reported-opinions.js` for asynchronous removal.


------------------------------------------------------------------------------------------------------------------------


## JavaScript Files

### `ADHD-button.js`

Manages the interactive “ADHD mode” button on the article card.  
Key behavior:

- Declares global `counter`, `timer_id`, and `duration = 10`.
- `count()` runs every second via `setInterval`, updates the button’s text/value with remaining seconds.
- When the countdown finishes:
  - Clears the interval.
  - Resets the counter.
  - Reverts button color and text to “ADHD OFF”.
  - Re-enables `#opinion-button` and `#random-button`.
- `change_color()` switches button styling to green (`bg-success`) and displays “ADHD ON”.
- `revert_color()` switches back to red (`bg-danger`) and displays “ADHD OFF”.
- `change_ADHD_state()`:
  - Disables the opinion and random buttons.
  - Calls `change_color()`.
  - Resets counter to 0 and starts a new interval.
- Event listener on `DOMContentLoaded` attaches the click handler to `#ADHD-button` if it exists.

### `reported-opinions.js`

Handles asynchronous moderation of reported opinions in the editor dashboard.  
Key behavior:

- On `DOMContentLoaded`, selects all `.remove-reported-button` elements and attaches click listeners.
- Also selects all `#keep-button` elements (note: repeated IDs are used but still functional) and attaches listeners.
- `delete_opinion(opinion_id, container)`:
  - Triggers the CSS hide animation on the parent container.
  - After `animationend`, removes the container from the DOM.
  - Sends a `POST` request to `/delete/opinion/<id>/` with a CSRF token.
- `keep_opinion(opinion_id, container)`:
  - Works identically but sends the request to `/keep/opinion/<id>/`.
  - Also animates and removes the container after the backend confirms the action.
- `getCookie(name)`:
  - Extracts the CSRF token from `document.cookie` to include in fetch headers.

  ## Python Files (Backend & Configuration)

### `admin.py`
Registers the application models (`Opinion`, `Label`, `Article`, `Image`, `Quiz`) with Django’s admin interface. Also creates a custom `UserAdmin` subclass (`AddEditorUser`) that adds the `is_editor` field to the user admin form, allowing staff to assign editor permissions directly from the admin panel.

### `forms.py`
Defines two custom form classes:

- **`PostNews`** – Used for creating a new `Article`. Includes fields for title, author name, three optional image URLs, content, popularity (as radio choices), and source URL.  
- **`PostOpinion`** – Used for creating a new `Opinion`. Includes title, author name, content, multiple label selection (`ModelMultipleChoiceField` rendered as checkboxes), a bias integer field, and an article selection via `ModelChoiceField` with a `TextInput` widget linked to a `<datalist>` for searchable autocomplete. The `__init__` method dynamically sets the querysets for `labels_select` and `article` to ensure fresh data on every request.

### `models.py`
Contains the database schema for the project:

- **`User`** – Extends `AbstractUser` with an `is_editor` boolean flag.
- **`Article`** – Stores news posts; linked to an editor (user), has title, author, content, popularity, source URL, view tracking (Many-to-Many with users), and creation timestamp.
- **`Opinion`** – User-submitted opinions tied to a specific article; includes title, writer, content, creation time, view tracking, reporter list (for moderation), and a bias score.
- **`Label`** – A tag model connected to opinions via a Many-to-Many relationship.
- **`Image`** – Stores image URLs linked to an article, with a flag for main image.
- **`Quiz`** – Simple model containing a question and answer for the interactive quiz feature.

### `urls.py`
Maps all URL endpoints to their corresponding view functions:

- `''` → `index`
- `login/`, `logout/`, `register/` → authentication views
- `specific/opinions/` and `all/opinions/` → opinion display views
- `create/post/` and `create/opinion/` → content creation views (editor/user)
- `random/post/` → random article shuffle
- `report/opinion/<id>/` → report an opinion
- `reported/opinions/` → editor dashboard for moderation
- `delete/opinion/<id>/` and `keep/opinion/<id>/` → asynchronous moderation endpoints
- `game/` and `get/quiz/api/` → quiz page and API endpoint

### `utils.py`
Provides helper functions, such as `add_viewers(user, article_id)`, which adds a user to the `views` Many-to-Many field of an `Article` to track unique viewers. This function is used in multiple views and ensures deduplicated view counting.

### `views.py`
Contains all the backend logic for the application:

- **Index** – Displays the latest article and tracks views for authenticated users.
- **Display opinions** – Renders either all opinions or those belonging to a specific article.
- **Random article** – Shows a random article and tracks views.
- **Create post** – Editor-only view that validates and saves a new `Article` along with its associated `Image` objects.
- **Create opinion** – Authenticated user view that saves a new `Opinion` and sets its labels.
- **Report opinion** – Adds the current user to the reporter list of an opinion.
- **Reported opinions** – Editor-only view listing opinions that have at least one report.
- **Delete/Keep opinion** – Editor-only endpoints that delete an opinion or clear its reporter list, returning a JSON response for asynchronous handling.
- **Quiz** – Renders the quiz page with a random question; API endpoint returns JSON data for the React component.
- **Authentication** – Handles login, logout, and registration with basic validation.


------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------

# How to run your application.
( These are depending on the type of operating systems )

python3 -m venv .env
source .env/bin/activate  
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py makemigrations timeline
python manage.py migrate
python manage.py loaddata timeline_reset_data
python manage.py runserver
Open browser with : http://127.0.0.1:8000/ or http://localhost:8000/
