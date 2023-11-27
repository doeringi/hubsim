from itertools import product
from jinja2 import Template
import yaml


_jinja_template_string = """You are {{name}}. Facts about yourself: {{socio_behavioral}}. Facts about the apartment: {{apartment}}. Your goal: {{target}}. Do not tell anyone the facts above. Don't talk about utilities or anything else, just the rental price. If you reach an agreement, say it like: price = x Euro, where x is the final price that you agreed on. If you didn't agree say: price = 0 Euro."""


def _load_yaml_data(subfolder: str, yaml_content: str):
    with open(
        f"assets/prompts/{subfolder}/{yaml_content}.yaml", "r", encoding="utf-8"
    ) as file:
        return yaml.safe_load(file)


def _load_landlord_config():
    return (
        _load_yaml_data("landlord", yaml_content)
        for yaml_content in [
            "name",
            "socio-behavioral",
            "target",
        ]
    )


def _load_renter_config():
    return (
        _load_yaml_data("renter", yaml_content)
        for yaml_content in ["name", "socio-behavioral", "target"]
    )


def _load_product_config():
    for item in _load_yaml_data("product", "apartment"):
        yield item


def all_landlord_variants():
    name, socio_behavioral, target = _load_landlord_config()
    apartment = _load_product_config()

    variants = product(name, socio_behavioral, target, apartment)

    return [
        (
            {
                "name_id": name["id"],
                "socio_behavioral_id": socio_behavioral["id"],
                "target_id": target["id"],
                "apartment_id": apartment["id"],
            },
            render_system_message(
                name["content"],
                socio_behavioral["content"],
                target["content"],
                apartment["content"],
            ),
        )
        for name, socio_behavioral, target, apartment in variants
    ]


def all_renter_variants():
    name, socio_behavioral, target = _load_renter_config()
    apartment = _load_product_config()

    variants = product(name, socio_behavioral, target, apartment)

    return [
        (
            {
                "name_id": name["id"],
                "socio_behavioral_id": socio_behavioral["id"],
                "target_id": target["id"],
                "apartment_id": apartment["id"],
            },
            render_system_message(
                name["content"],
                socio_behavioral["content"],
                target["content"],
                apartment["content"],
            ),
        )
        for name, socio_behavioral, target, apartment in variants
    ]


def all_variants():
    landlord_variants = all_landlord_variants()
    renter_variants = all_renter_variants()

    all_variants = product(landlord_variants, renter_variants)

    return [(variant) for variant in all_variants]


def single_factor_variants():
    apartment = _load_product_config()
    # landlord_renter = landlord_renter_combination()

    landlord_name, landlord_socio_behavioral, landlord_target = _load_landlord_config()
    renter_name, renter_socio_behavioral, renter_target = _load_renter_config()

    landlord_renter = [
        (
            {
                "name_id": landlord_name[0]["id"],
                "socio_behavioral_id": landlord_socio_behavioral[0]["id"],
                "target_id": landlord_target[0]["id"],
            },
            {
                "name_id": renter_name[0]["id"],
                "socio_behavioral_id": renter_socio_behavioral[0]["id"],
                "target_id": renter_target[0]["id"],
            },
        )
    ]

    factor_variants = product(landlord_renter, apartment)

    return [
        (
            variant,
            {
                "landlord_system_message": render_system_message(
                    landlord_name[0]["content"],
                    landlord_socio_behavioral[0]["content"],
                    landlord_target[0]["content"],
                    variant[1]["content"],
                ),
                "renter_system_message": render_system_message(
                    renter_name[0]["content"],
                    renter_socio_behavioral[0]["content"],
                    renter_target[0]["content"],
                    variant[1]["content"],
                ),
            },
        )
        for variant in factor_variants
    ]


def render_system_message(
    name: str, socio_behavioral: str, target: str, apartment: str
) -> str:
    jinja_template = Template(_jinja_template_string)

    return jinja_template.render(
        name=name,
        socio_behavioral=socio_behavioral,
        target=target,
        apartment=apartment,
    )


# example all variants
all = single_factor_variants()
print(len(all))
print(all)
# print(all[0][0])
# print(all[0][0][1])
