The error message indicates that there is a problem with the XML syntax in the `menu_config.xml` file, specifically on line 37 at column 52. This kind of error typically occurs due to an issue such as an unescaped character, a missing quote, or incorrect XML formatting.

Let’s go over the possible causes and how to fix them:

### Common Causes:
1. **Unescaped Characters**: Special characters like `&`, `<`, and `>` must be properly escaped in XML.
2. **Incorrect Quotes**: Ensure that all attribute values are enclosed in either single (`'`) or double (`"`) quotes.
3. **Malformed JSON**: Since you are using JSON strings within the XML (for lists and maps), ensure that the JSON is correctly formatted.

### Steps to Fix:
1. **Check Line 37**: Open the `menu_config.xml` file and navigate to line 37. Look for any unescaped characters, mismatched quotes, or malformed JSON.
2. **Correct JSON Format**: Ensure that the JSON strings for list and map parameters are correctly formatted. For example, make sure that double quotes (`"`) are used around keys and values in JSON.

### Example Fix:
If the error is related to a map parameter, it could look like this:

**Incorrect**:
```xml
<param name="map_param" default="{"key1": "value1", "key2": "value2"}" type="map"/>
```

**Correct**:
```xml
<param name="map_param" default="{&quot;key1&quot;: &quot;value1&quot;, &quot;key2&quot;: &quot;value2&quot;}" type="map"/>
```

In XML, double quotes inside an attribute value must be escaped as `&quot;`.

### If You Need to Escape Special Characters:
- `&` -> `&amp;`
- `<` -> `&lt;`
- `>` -> `&gt;`
- `"` -> `&quot;`
- `'` -> `&apos;`

### Additional Check:
After correcting the XML, validate the entire file to ensure there are no other syntax errors. Many XML editors or IDEs provide built-in validation tools.

Would you like to upload the `menu_config.xml` file so I can take a closer look and help you resolve the issue?