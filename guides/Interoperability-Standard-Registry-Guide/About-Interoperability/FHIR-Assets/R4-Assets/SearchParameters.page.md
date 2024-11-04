<label>
    <input type="checkbox" id="ukcore-checkbox" checked>
    Show UKCore Items
    </label>
    <br>
    <label>
    <input type="checkbox" id="nhsengland-checkbox" checked>
    Show NHSEngland Items
    </label>

    
<script>
    const ukcoreCheckbox = document.getElementById('ukcore-checkbox');
    const nhsenglandCheckbox = document.getElementById('nhsengland-checkbox');

    ukcoreCheckbox.addEventListener('change', function() {
        const ukcoreItems = document.querySelectorAll('.ukcore');
        ukcoreItems.forEach(item => {
        if (ukcoreCheckbox.checked) {
            item.classList.remove('hidden');
        } else {
            item.classList.add('hidden');
        }
        });
    });

    nhsenglandCheckbox.addEventListener('change', function() {
        const nhsenglandItems = document.querySelectorAll('.nhsengland');
        nhsenglandItems.forEach(item => {
        if (nhsenglandCheckbox.checked) {
            item.classList.remove('hidden');
        } else {
            item.classList.add('hidden');
        }
        });
    });
    </script>

    
## SearchParameters


<a href="https://simplifier.net/NHS-England-Programme-Implementation-Guides/England-Extension-OrganisationRole-ActiveRoleCode" class="child-title">
<div class="title">England-Extension-OrganisationRole-ActiveRoleCode</div>
<div class="description">
  0.0.2 &nbsp;&nbsp;&nbsp;&nbsp;
  2024-02-14 &nbsp;&nbsp;&nbsp;&nbsp;
<span class="status draft">draft</span> &nbsp;&nbsp;&nbsp;&nbsp;
</div>
</a>
<a href="https://simplifier.net/NHS-England-Programme-Implementation-Guides/England-Extension-OrganisationRole-RoleCode" class="child-title">
<div class="title">England-Extension-OrganisationRole-RoleCode</div>
<div class="description">
  0.0.2 &nbsp;&nbsp;&nbsp;&nbsp;
  2024-02-14 &nbsp;&nbsp;&nbsp;&nbsp;
<span class="status draft">draft</span> &nbsp;&nbsp;&nbsp;&nbsp;
</div>
</a>
<a href="https://simplifier.net/NHS-England-Programme-Implementation-Guides/England-Extension-TypedDateTime-LastChangeDate" class="child-title">
<div class="title">England-Extension-TypedDateTime-LastChangeDate</div>
<div class="description">
  0.0.2 &nbsp;&nbsp;&nbsp;&nbsp;
  2024-02-14 &nbsp;&nbsp;&nbsp;&nbsp;
<span class="status draft">draft</span> &nbsp;&nbsp;&nbsp;&nbsp;
</div>
</a>
<a href="https://simplifier.net/NHS-England-Programme-Implementation-Guides/England-FlagCategory" class="child-title">
<div class="title">England-FlagCategory</div>
<div class="description">
  0.4.0 &nbsp;&nbsp;&nbsp;&nbsp;
  2024-02-14 &nbsp;&nbsp;&nbsp;&nbsp;
<span class="status active">active</span> &nbsp;&nbsp;&nbsp;&nbsp;
</div>
</a>
<a href="https://simplifier.net/NHS-England-Programme-Implementation-Guides/England-FlagCode" class="child-title">
<div class="title">England-FlagCode</div>
<div class="description">
  0.1.0 &nbsp;&nbsp;&nbsp;&nbsp;
  2024-02-14 &nbsp;&nbsp;&nbsp;&nbsp;
<span class="status draft">draft</span> &nbsp;&nbsp;&nbsp;&nbsp;
</div>
</a>
<a href="https://simplifier.net/NHS-England-Programme-Implementation-Guides/England-FlagDetail" class="child-title">
<div class="title">England-FlagDetail</div>
<div class="description">
  0.4.0 &nbsp;&nbsp;&nbsp;&nbsp;
  2024-02-14 &nbsp;&nbsp;&nbsp;&nbsp;
<span class="status active">active</span> &nbsp;&nbsp;&nbsp;&nbsp;
</div>
</a>
</div><!--TEST2-->

---


