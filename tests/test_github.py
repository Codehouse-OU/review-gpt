import pytest

from reviewgpt.configuration import Configuration
from reviewgpt.repository.github import GitHubService

@pytest.fixture
def client():
    return GitHubService(Configuration())

def test_post_process_comments(client):
    code_diff = """
diff --git a/src/main/java/ee/codehouse/foodbook/web/rest/MealPlanResource.java b/src/main/java/ee/codehouse/foodbook/web/rest/MealPlanResource.java
new file mode 100644
index 0000000..3062b98
--- /dev/null
+++ b/src/main/java/ee/codehouse/foodbook/web/rest/MealPlanResource.java
@@ -0,0 +1,32 @@
+package ee.codehouse.foodbook.web.rest;
+
+import ee.codehouse.foodbook.service.MealPlanFactory;
+import ee.codehouse.foodbook.service.MealPlanService;
+import ee.codehouse.foodbook.service.dto.DailyMealPlan;
+import java.util.Map;
+import java.util.logging.Logger;
+import org.springframework.http.ResponseEntity;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PathVariable;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RestController;
+
+@RestController
+@RequestMapping("/api/meal-plan")
+public class MealPlanResource {
+
+    private static final Logger LOG = Logger.getLogger(MealPlanResource.class.getName());
+
+    private final MealPlanFactory mealPlanFactory;
+
+    public MealPlanResource(MealPlanFactory mealPlanFactory) {
+        this.mealPlanFactory = mealPlanFactory;
+    }
+
+    @GetMapping('/get-meal-plan/{days}')
+    public ResponseEntity<Map<Integer, DailyMealPlan>> getMealPlan(@PathVariable int days) {
+        LOG.info("Getting meal plan for " + days + " days");
+        MealPlanService mealPlanService = mealPlanFactory.getMealPlanService("Randomized");
+        return ResponseEntity.ok(mealPlanService.getMealPlan(days));
+    }
+}
    """
    comments = """[{
"body": "Consider including the type of meal plan service as a parameter in the getMealPlan method to avoid hardcoding the service type",
"path": "src/main/java/ee/codehouse/foodbook/web/rest/MealPlanResource.java",
"line": " @GetMapping('/get-meal-plan/{days}')",
"position": 0
}]"""
    result = client.post_process(code_diff, comments)

    assert result[0]["position"] == 26
