/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { Thread } from "@mail/core/common/thread_model";
import { _t } from "@web/core/l10n/translation"; // ضروري لاستخدام _t

patch(Thread.prototype, {
    /**
     * @override
     */
    async post(body, postData = {}, extraData = {}) {
        const publicName = document.getElementById('public_name');
        const publicEmail = document.getElementById('public_email');

        // Ensure values exist or short-circuit
        if (publicName && publicEmail) {
            const nameValue = publicName.value.trim();
            const emailValue = publicEmail.value.trim();

            if (!nameValue || !emailValue) {
                alert(_t("Please provide both your name and email, or log in, to post a comment."));
                return;
            }
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(emailValue)) {
                alert(_t("Please enter a valid email address."));
                publicEmail.focus();
                return;
            }
        }

        // Get Odoo's post parameters
        const params = await this.store.getMessagePostParams({ body, postData, thread: this });
        Object.assign(params, extraData);

        // Append author info to post data
        if (publicName && publicName.value) {
            params.post_data = {
                ...params.post_data,
                public_author_name: publicName.value,
                public_author_email: document.getElementById('public_email')?.value,
                public_author_website: document.getElementById('public_website')?.value,
            };
        }

        return super.post(body, postData, params);
    }
});