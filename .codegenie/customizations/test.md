# Testing Practices Cheat Sheet

## Testing Libraries and Frameworks

- Jest: Primary testing framework in use
- Mockito: Used for mocking in Java tests
- PowerMock: Used for advanced mocking scenarios

## Mocking and Stubbing Strategies

### Jest Mocks

```javascript
jest.mock('module-name');
const mockFunction = jest.fn();
```

### Mockito Mocks

```java
@Mock
private DependencyClass mockDependency;

when(mockDependency.method()).thenReturn(expectedValue);
```

### PowerMock for Static Methods

```java
@RunWith(PowerMockRunner.class)
@PrepareForTest({StaticClass.class})
public class TestClass {
    @Test
    public void testStaticMethod() {
        PowerMockito.mockStatic(StaticClass.class);
        when(StaticClass.staticMethod()).thenReturn(expectedValue);
    }
}
```

## Fake Implementations

### In-Memory Database for Testing

```java
public class InMemoryDatabase implements Database {
    private Map<String, Object> storage = new HashMap<>();

    @Override
    public void save(String key, Object value) {
        storage.put(key, value);
    }

    @Override
    public Object retrieve(String key) {
        return storage.get(key);
    }
}
```

### Fake HTTP Client

```javascript
class FakeHttpClient {
    async get(url) {
        // Return predefined responses based on URL
    }

    async post(url, data) {
        // Store posted data and return mock response
    }
}
```

## Test Organization

- Use `describe` blocks to group related tests
- Use `beforeEach` and `afterEach` for setup and teardown
- Name tests descriptively using `it` or `test` functions

```javascript
describe('UserService', () => {
    let userService;
    
    beforeEach(() => {
        userService = new UserService();
    });

    it('should create a new user', () => {
        // Test implementation
    });
});
```

## Assertion Styles

- Use `expect` statements in Jest
- Use AssertJ for fluent assertions in Java

```javascript
expect(result).toBe(expectedValue);
expect(array).toContain(item);
```

```java
assertThat(result).isEqualTo(expectedValue);
assertThat(list).contains(element);
```

## Code Coverage

- Aim for high code coverage (e.g., >80%)
- Use Jest's coverage reporting feature
- Exclude certain files or directories from coverage reports

## Best Practices

1. Test one thing per test case
2. Use descriptive test names
3. Avoid test interdependence
4. Mock external dependencies
5. Use setup and teardown methods for common operations
6. Test both positive and negative scenarios
7. Use parameterized tests for multiple inputs
8. Keep tests fast and isolated

## Continuous Integration

- Run tests automatically on each commit
- Fail the build if tests don't pass
- Generate and store test reports