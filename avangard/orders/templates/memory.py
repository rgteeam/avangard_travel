{% extends "base.html" %}
{% load staticfiles %}
{% block title %}Создать заказ{% endblock %}

{% block style %}
    <script src='{% static 'js/jquery.min.js' %}' , integrity='' , crossorigin='anonymous'></script>
    <script type="text/javascript" src="{% static 'js/moment-with-locales.min.js' %}"></script>
    <script type="text/javascript" src="{% static 'js/bootstrap-datepicker.min.js' %}"></script>
    <script type="text/javascript">

        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

    </script>

    <script type="text/javascript">
        var seance_full_ticket_price = 0;
        var seance_reduce_ticket_price = 0;
    </script>

    <link rel="stylesheet" href="{% static 'css/bootstrap-datepicker3.min.css' %}">

{% endblock %}

{% block content %}
    <div class="container" style="width: 85%">

        <div class="panel-heading">
            <div class="panel-title text-center">
                {% if type == 'edit' %}
                    <h1 class="title">{{ museum.name }} - редактировать заказ</h1>
                {% else %}
                    <h1 class="title">{{ museum.name }} – создать заказ</h1>
                {% endif %}
                <hr/>
            </div>
        </div>

        <form action='' method="post"> {% csrf_token %}
            <div class="row">
                <div class="col-sm-8">
                    <div class="card">
                        <div class="card-header">Данные о заказе</div>
                        <div class="card-block">

                            {{ form.museum.as_hidden }}
                            {{ form.fullticket_store.as_hidden }}
                            {{ form.reduceticket_store.as_hidden }}

                            <div class="form-group">
                                <div id="datepicker"></div>
                            </div>

                            {% if form.non_field_errors %}
                                <div class="alert alert-danger" role="alert">
                                    {{ form.non_field_errors.0 }}.
                                </div>
                            {% endif %}

                            <div class="form-group">
                                <label for="id_seance">Доступное время:</label>
                                {{ form.seance }}
                            </div>


                            <div class="form-group {% if form.fullticket_count.errors or form.non_field_errors %} has-danger {% endif %}">

                                <label id="id_fullticket_count_label" class="form-control-label"
                                       for="id_fullticket_count">Количество взрослых билетов
                                    (1 шт.
                                    -
                                    р.):</label>

                                {{ form.fullticket_count }}

                                {% if form.fullticket_count.errors %}
                                    <div class="form-control-feedback">{{ form.fullticket_count.errors }}</div>
                                {% endif %}

                            </div>

                            <div class="form-group {% if form.reduceticket_count.errors or form.non_field_errors %} has-danger {% endif %}">

                                <label id="id_reduceticket_count_label" class="form-control-label"
                                       for="id_reduceticket_count">Количество льготных
                                    билетов (1 шт.
                                    -
                                    р.):</label>

                                {{ form.reduceticket_count }}

                                {% if form.reduceticket_count.errors %}
                                    <div class="form-control-feedback">{{ form.reduceticket_count.errors }}</div>
                                {% endif %}

                            </div>

                            <div class="checkbox">
                                <label>{{ form.audioguide }} Аудиогид (1 шт. - {{ museum.audioguide_price }} р.)</label>
                            </div>

                            <div class="checkbox">
                                <label>{{ form.accompanying_guide }} Сопровождающий гид (стоимость
                                    - {{ museum.accompanying_guide_price }} р.)</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-4">
                    <div class="card">

                        <div class="card-block">
                            <h3 class="card-title">Стоимость</h3>
                            <p>Взрослые билеты: <span id="fullticket_price">0</span> руб.</p>
                            <p>Льготные билеты: <span id="reduceticket_price">0</span> руб.</p>
                            <p>Аудиогиды: <span id="audioguide_price">0</span> руб.</p>
                            <p>Сопровождающий гид: <span id="accompanying_guide_price">0</span> руб.</p>
                            <h4 class="card-title">Итого: <span id="total_price">0</span> руб.</h4>
                        </div>
                    </div>
                </div>
                <div class="col-sm-8">
                    <div class="card">
                        <div class="card-header">Контактные данные</div>
                        <div class="card-block">
                            <div class="form-group">
                                <label for="name">ФИО:</label>
                                {{ form.name }}
                            </div>

                            <div class="form-group">
                                <label for="email">Email:</label>
                                {{ form.email }}
                            </div>

                            <div class="form-group">
                                <label for="phone">Телефон:</label>
                                {{ form.phone }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>


            <!--
            <div class="form-group">
                <label for="image">Изображение:</label>
                <input type="file" class="form-control" id="image">
            </div>
            -->
            <div class="form-group">
                <button type="submit" class="btn btn-primary btn-lg btn-block" style="margin-top: 20px">
                    {% if type == 'edit' %}Изменить{% else %}Создать{% endif %}
                </button>
            </div>
        </form>


    </div>

    <script type="text/javascript">

        function get_ticket_price(ticket_store) {
            var ticket_data = JSON.parse(ticket_store.replace(/&quot;/g, '"'));
            var sum = 0;
            $.each(ticket_data, function (key, value) {
                $.each(value, function (key, value) {
                    sum += parseInt(key) * parseInt(value);
                });
            });
            console.log("SUM = " + sum);
            return sum;
        }

        function update_fullticket_price(fullticket_exist) {
            var fullticket_new = parseInt($('#id_fullticket_count').val());
            if (fullticket_new >= fullticket_exist) {
                return (fullticket_new - fullticket_exist) * seance_full_ticket_price;
            }
            if (fullticket_new < fullticket_exist) {
                return (fullticket_new - fullticket_exist) * seance_full_ticket_price;
            }
{#            return parseInt($('#id_reduceticket_count').val()) * seance_reduce_ticket_price;#}
        }

        function update_reduceticket_price() {
            return parseInt($('#id_reduceticket_count').val()) * seance_reduce_ticket_price;
        }

        function get_audioguide_price() {
            if (document.getElementById('id_audioguide').checked) {
                var total_count = parseInt($('#id_reduceticket_count').val()) + parseInt($('#id_fullticket_count').val());
                audioguide_price = total_count * {{ museum.audioguide_price }};
            } else {
                audioguide_price = 0;
            }
            return audioguide_price;
        }

        function get_accompanying_guide_price() {
            if (document.getElementById('id_accompanying_guide').checked) {
                accompanying_guide_price = {{ museum.accompanying_guide_price }};
            } else {
                accompanying_guide_price = 0;
            }
            return accompanying_guide_price;
        }

{#        var full_ticket_price = get_ticket_price("{{ fullticket_store }}");#}
{#        var reduce_ticket_price = get_ticket_price("{{ reduceticket_store }}");#}
        var audioguide_price = get_audioguide_price();
        var accompanying_guide_price = get_accompanying_guide_price();

        function get_loaded_prices() {
            full_ticket_price = get_ticket_price("{{ fullticket_store }}");
            reduce_ticket_price = get_ticket_price("{{ reduceticket_store }}");
            update_audio_guide_price();
            get_total_price();
        }

        $('#id_fullticket_count').keyup(function () {
{#            console.log(update_fullticket_price("{{ instance.fullticket_count }}"));#}
            full_ticket_price += update_fullticket_price("{{ instance.fullticket_count }}");
            console.log(full_ticket_price);
            update_audio_guide_price();
            get_total_price()
        });

        $('#id_reduceticket_count').keyup(function () {
            reduce_ticket_price += update_reduceticket_price();
            update_audio_guide_price();
            get_total_price();
        });

        $(document).on('change', '#id_accompanying_guide', function () {
            accompanying_guide_price = get_accompanying_guide_price();
            get_total_price();
        });

        $(document).on('change', '#id_audioguide', update_audio_guide_price);

        function update_audio_guide_price() {
            audioguide_price = get_audioguide_price();
            get_total_price();
        }

        function get_total_price() {
            totalSum = 0;
            totalSum = full_ticket_price + reduce_ticket_price + audioguide_price + accompanying_guide_price;
            $("#total_price").text(totalSum);
            $('#fullticket_price').text(full_ticket_price);
            $('#reduceticket_price').text(reduce_ticket_price);
            $('#audioguide_price').text(audioguide_price);
            $('#accompanying_guide_price').text(accompanying_guide_price);
        }

    </script>

    <script type="text/javascript">
        $(function () {
            $('#datepicker').datepicker({format: 'dd-mm-yyyy'});

            {% if date != None %}
                var date = "{{ date|date:"d-m-Y" }}";
            {% else %}
                var date = getDate();
            {% endif %}

            $('#datepicker').on('changeDate', function () {
                console.log("changed");
                date = $('#datepicker').datepicker('getFormattedDate');
                console.log(date);
                $.ajax
                ({
                    type: "Get",
                    url: "/orders/get_seances/",
                    data: "date=" + date + "&museum_id={{ museum.pk }}",
                    success: function (data) {
                        var output = [];
                        var selected = undefined;

                        $.each(data['seances'], function (key, value) {
                            output.push('<option value="' + value.value + '">' + value.text + '</option>');
                            {% if form.seance.value != None %}
                                var selectValue = {{ form.seance.value }}
                                if (selectValue == value.value) {
                                    selected = selectValue;
                                }
                            {% endif %}
                        });

                        if (output.length == 0) {
                            output.push('<option value="" selected="">Нет сеансов</option>');
                            setup_seance_price_labels(0, 0)
                        } else {
                            setup_selected_seance(data['seances'][0].value)
                        }

                        $('#id_seance').html(output.join(''));

                        if (selected !== undefined) {
                            $('#id_seance').val(selected);
                        }

                    }
                });
            });

            $('#datepicker').datepicker('setDate', date);
        });

        function setup_selected_seance(val) {
            $.ajax
            ({
                type: "Post",
                url: "/orders/seance_selected/",
                data: "seance_id=" + val
            }).done(function (result) {
                setup_seance_price_labels(result.seance.full_price, result.seance.reduce_price)
            })
        }

        function setup_seance_price_labels(full_price, reduce_price) {
            seance_full_ticket_price = full_price;
            seance_reduce_ticket_price = reduce_price;
            get_loaded_prices();
            $("#id_fullticket_count_label").text("Количество взрослых билетов(1 шт. - " + seance_full_ticket_price + " р.):");
            $("#id_reduceticket_count_label").text("Количество льготных билетов(1 шт. - " + seance_reduce_ticket_price + " р.):");
        }

        $('#id_seance').on('change', function (e) {
            var optionSelected = $("option:selected", this);
            setup_selected_seance(this.value)
        });


        function getDate() {
            var d = new Date();
            var currDate = d.getDate();
            var currMonth = d.getMonth() + 1;
            var currYear = d.getFullYear();
            var dateStr = currDate + "-" + currMonth + "-" + currYear;
            return dateStr;
        }
    </script>

{% endblock %}
{% block footer %}
{% endblock %}