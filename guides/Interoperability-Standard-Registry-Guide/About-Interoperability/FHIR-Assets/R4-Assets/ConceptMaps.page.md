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

    
## ConceptMaps

<div class="status-container">
<ul>

<a href="https://simplifier.net/HL7FHIRUKCoreR4/UKCore-AdministrativeGender" class="child-title">
<div class="title">UKCore-AdministrativeGender</div>
<div class="description">
  2.0.0 &nbsp;&nbsp;&nbsp;&nbsp;
  2021-09-10 &nbsp;&nbsp;&nbsp;&nbsp;
<span class="status retired">retired</span> &nbsp;&nbsp;&nbsp;&nbsp;
</div>
</a>
<a href="https://simplifier.net/HL7FHIRUKCoreR4/UKCore-ConditionEpisodicity" class="child-title">
<div class="title">UKCore-ConditionEpisodicity</div>
<div class="description">
  2.0.0 &nbsp;&nbsp;&nbsp;&nbsp;
  2022-12-16 &nbsp;&nbsp;&nbsp;&nbsp;
<span class="status retired">retired</span> &nbsp;&nbsp;&nbsp;&nbsp;
</div>
</a>
<a href="https://simplifier.net/HL7FHIRUKCoreR4/UKCore-MaritalStatus" class="child-title">
<div class="title">UKCore-MaritalStatus</div>
<div class="description">
  2.0.0 &nbsp;&nbsp;&nbsp;&nbsp;
  2021-09-10 &nbsp;&nbsp;&nbsp;&nbsp;
<span class="status retired">retired</span> &nbsp;&nbsp;&nbsp;&nbsp;
</div>
</a>
</div>

---


